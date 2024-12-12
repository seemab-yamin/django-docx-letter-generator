from docxtpl import DocxTemplate


def json_to_docx(context, template_file, output_file):
    doc = DocxTemplate(template_file=template_file)

    context["client_occupation"] = context["client_occupation"].lower()
    if (
        context["client_occupation"].startswith("a")
        or context["client_occupation"].startswith("e")
        or context["client_occupation"].startswith("i")
        or context["client_occupation"].startswith("o")
        or context["client_occupation"].startswith("u")
    ):
        context["client_occupation"] = "an " + context["client_occupation"]
    else:
        context["client_occupation"] = "a " + context["client_occupation"]

    existing_plan_phrase_template = (
        "an existing policy with {} {}, and a coverage of {}"
    )

    if not context["existing_plans"]:
        context["existing_plans"] = "no existing plans"
    else:
        context["existing_plans"] = [
            existing_plan_phrase_template.format(*item)
            for item in context["existing_plans"].values()
        ]

        if len(context["existing_plans"]) == 2:
            context["existing_plans"] = " and ".join(context["existing_plans"])
        elif len(context["existing_plans"]) > 2:
            last_record = context["existing_plans"][-1]
            context["existing_plans"] = ", ".join(context["existing_plans"][:-1])
            context["existing_plans"] = (
                context["existing_plans"] + ", and " + last_record
            )
        else:
            context["existing_plans"] = ", ".join(context["existing_plans"])

    # process common_insurance_needs_considerations
    context["common_insurance_needs_considerations"] = [
        key for key in context["common_insurance_needs"].keys()
    ]
    if len(context["common_insurance_needs_considerations"]) == 2:
        context["common_insurance_needs_considerations"] = " and ".join(
            context["common_insurance_needs_considerations"]
        )
    elif len(context["common_insurance_needs_considerations"]) > 2:
        last_record = context["common_insurance_needs_considerations"][-1]
        context["common_insurance_needs_considerations"] = ", ".join(
            context["common_insurance_needs_considerations"][:-1]
        )
        context["common_insurance_needs_considerations"] = (
            context["common_insurance_needs_considerations"] + ", and " + last_record
        )
    else:
        context["common_insurance_needs_considerations"] = ", ".join(
            context["common_insurance_needs_considerations"]
        )

    # process common_insurance_needs
    context["common_insurance_needs"] = [
        key + ": " + value for key, value in context["common_insurance_needs"].items()
    ]

    doc.render(context=context)

    doc.save(output_file)
