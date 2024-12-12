import base64
import json
import os

from django.conf import settings
from django.contrib import messages
from django.http import FileResponse, HttpResponseNotFound
from django.shortcuts import render

from .docx_generator import json_to_docx


def download_file(request, encoded_path):
    # Decode the Base64-encoded path
    file_path = base64.urlsafe_b64decode(encoded_path.encode()).decode()

    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            f = open(file_path, "rb")
            response = FileResponse(
                f,
                content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
            response["Content-Disposition"] = (
                f'attachment; filename="{os.path.basename(file_path)}"',
            )
            return response
    else:
        return HttpResponseNotFound(f"File not found:{file_path}")


def render_form(request):
    if request.method == "POST":
        try:
            submitted_data = request.POST.dict()
            file_name = "form_results.docx"
            file_path = os.path.join(settings.MEDIA_ROOT, file_name)

            submitted_data.pop("csrfmiddlewaretoken")

            template_file = os.path.join(
                settings.STATIC_ROOT, "form_handler/files/Personal_PAR.docx"
            )
            if submitted_data.get("existing plans") == "No":
                existing_plans = False
            else:
                existing_plans = {
                    key: value
                    for key, value in submitted_data.items()
                    if "existing plan" in key and key != "existing plans"
                }

                new_existing_plans = {}
                for key, value in existing_plans.items():
                    if not value:
                        continue
                    i = str(key.split("_")[-1])
                    if i in new_existing_plans.keys():
                        new_existing_plans[i].append(value)
                    else:
                        new_existing_plans[i] = [value]
                existing_plans = new_existing_plans

            if submitted_data.get("FIB-plan provider"):
                plan_provider = submitted_data["FIB-plan provider"]
            else:
                plan_provider = submitted_data["plan provider"]

            plan_funding_period = submitted_data["plan funding period"]

            common_insurance_needs = {
                value.split(":")[0]: value.split(":")[1]
                for key, value in submitted_data.items()
                if key.startswith("common insurance needs")
            }

            # TODO
            context = {
                "client_name": submitted_data["client name"],
                "client_occupation": submitted_data["client occupation"],
                "existing_plans": existing_plans,
                "common_insurance_needs": common_insurance_needs,
                "plan_provider": plan_provider,
                "plan_funding_period": plan_funding_period,
                "plan_coverage": submitted_data["plan coverage"],
                "policy_number": submitted_data["policy number"],
                "plan_type": submitted_data["plan_type"],
                "plan_type_reasoning": submitted_data["plan_type_reasoning"],
                "agent_name": submitted_data["agent name"],
            }

            json_to_docx(
                context=context,
                template_file=template_file,
                output_file=file_path,
            )

            messages.success(request, "The operation was successful.")
            return render(request, "download.html", context={"file_name": file_name})
        except Exception as err:
            print(f"Exception Occurred:\t{err}")
            messages.error(request, "Couldn't Generate Docx File. Try Again!")

    input_file_path = os.path.join(
        settings.BASE_DIR, "form_handler", settings.INPUT_FORM_TEMPLATE
    )
    with open(input_file_path, "r") as file:
        form_templates = json.load(file)

    return render(
        request, "render_form.html", context={"form_templates": form_templates}
    )
