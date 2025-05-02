from utils.modelAI import gemini_model
import json
from db import get_db


def time_management(active_user, answers):
    prompt = f"""
    Bạn là một trợ lý lập kế hoạch AI thông minh.
    Bạn sẽ giúp người dùng lên kế hoạch cho tuần đầu tiên của họ dựa trên thông tin họ cung cấp.

    Dữ liệu người dùng:
    {json.dumps({"answers": answers, "active_user": active_user}, ensure_ascii=False)}
    Nếu người dùng không cung cấp thông tin nào, hãy sử dụng thông tin mặc định sau:
        🔹 Từ Thứ Hai đến Thứ Sáu:
        - Tập trung vào năng suất cao: học tập, làm việc, thể chất.
        - Có thời gian nghỉ xen kẽ để tránh quá tải.
        - Bắt đầu sau giờ thức dậy và kết thúc trước giờ ngủ.
        - Đầy đủ 3 bữa ăn trong ngày
        🔹 Thứ Bảy và Chủ Nhật:
        - Lịch nhẹ nhàng, tập trung thư giãn, nghỉ ngơi.
        - Vẫn có thể duy trì tập luyện nhẹ và tổng kết tuần.
        - Đầy đủ 3 bữa ăn trong ngày
        - Bắt đầu sau giờ thức dậy và kết thúc trước giờ ngủ.
    Còn người dùng cung cấp thông tin thời khóa biểu trước đó của họ thì lên lịch thế này
        - Lên lịch theo kế hoạch họ cung cấp.
        🔹 Thứ Hai đến thứ Sáu:
            - Sắp xếp phù hợp với giờ người dùng cung cấp, không thay đổi những giờ họ cung cấp.
            - Tập trung vào năng suất cao: học tập, làm việc, thể chất.
            - Có thời gian nghỉ xen kẽ để tránh quá tải.
            - Bắt đầu sau giờ thức dậy và kết thúc trước giờ ngủ.
            - Đầy đủ 3 bữa ăn trong ngày
        🔹 Thứ Bảy và Chủ Nhật:
            - Đầy đủ 3 bữa ăn trong ngày
            - Lịch nhẹ nhàng, tập trung thư giãn, nghỉ ngơi.
            - Vẫn có thể duy trì tập luyện nhẹ và tổng kết tuần.
            - Bắt đầu sau giờ thức dậy và kết thúc trước giờ ngủ.
    🔹 Lưu ý:
    - Lên kế hoạch tuần dựa trên thứ tự ưu tiên mục tiêu người dùng cung cấp.
    - Tất cả thời gian hoạt động cần nằm trong khung từ giờ thức dậy đến giờ ngủ.
    - Mỗi ngày nên có ít nhất 1–3 khung giờ nghỉ hoặc thư giãn.

    📦 Yêu cầu:
    - Trả về kết quả ở định dạng JSON, đúng cấu trúc sau:

    {{
    
        "monday": [
        {{ "time": "06:30-07:15", "activity": "Tập thể dục buổi sáng", "note": "Cardio nhẹ tại nhà" }},
        ...
        ],
        ...
        "sunday": [ ... ]
    
    }}

    Trả về **chỉ nội dung JSON thuần**, không thêm mô tả, không sử dụng markdown (```), không thêm đoạn văn bản nào khác.
    """

    model = gemini_model()
    response = model.generate_content(prompt)

    response_text = response.text.strip()

    if response_text.startswith("```json"):
        response_text = response_text.replace("```json", "").replace("```", "").strip()

    try:
        plan_data = json.loads(response_text)
    except json.JSONDecodeError as e:
        print("❌ Lỗi parse JSON:", e)
        return None

    db = get_db()
    collection = db["TimePlans"]

    result = collection.insert_one(
        {
            "user": active_user,
            "plan": plan_data,
        }
    )

    print(f"✅ Đã lưu kế hoạch với ID: {result.inserted_id}")
    return result.inserted_id
