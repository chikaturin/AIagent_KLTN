from flask import Blueprint, request, jsonify
from services.time_management import time_management
import traceback

timeplan_bp = Blueprint("timeplan_bp", __name__)


@timeplan_bp.route("/generate-plan", methods=["POST"])
def generate_plan():
    try:
        data = request.get_json()
        active_user = data.get("active_user")
        answers = data.get("answers")
        if not request.is_json:
            return (
                jsonify({"error": "Yêu cầu phải có Content-Type: application/json"}),
                415,
            )

        if not active_user or not answers:
            return jsonify({"error": "Thiếu user hoặc answers"}), 400

        inserted_id = time_management(active_user, answers)

        if not inserted_id:
            return jsonify({"error": "Lỗi khi tạo kế hoạch"}), 500

        return (
            jsonify({"message": "Tạo kế hoạch thành công", "id": str(inserted_id)}),
            200,
        )

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
