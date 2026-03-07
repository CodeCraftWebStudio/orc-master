from ..user_model import RoleType

EXECUTIVE_ROLES = {
    "president": {
        "label": "President",
        "role_type": RoleType.ADMIN,
        "code": "A1K9-M3T6-Q2V8"
    },
    "vicePresident": {
        "label": "Vice President",
        "role_type": RoleType.EDITING_EXEC,
        "code": "D4F7-L1P9-C8J2"
    },
    "commandant": {
        "label": "Parade Commandant",
        "role_type": RoleType.EDITING_EXEC,
        "code": "M5B2-H8N1-K3Q7"
    },
    "assistantCommandant": {
        "label": "Assistant Commandant",
        "role_type": RoleType.NON_EDITOR_EXEC,
        "code": "E3X7-V1Q4-K6J8"
    },
    "secretary": {
        "label": "General Secretary",
        "role_type": RoleType.EDITING_EXEC,
        "code": "R6P4-T2J9-L1C8"
    },
    "assistantSecretary": {
        "label": "Assistant General Secretary",
        "role_type": RoleType.NON_EDITOR_EXEC,
        "code": "K5J1-P7M4-L8V2"
    },
    "socialDirector": {
        "label": "Social Director",
        "role_type": RoleType.NON_EDITOR_EXEC,
        "code": "V9K1-Q3M7-P5B2"
    },
    "technicalDirector": {
        "label": "Technical Director",
        "role_type": RoleType.NON_EDITOR_EXEC,
        "code": "C2H6-F9L4-N3V8"
    },
    "assistantTechnicalDirector": {
        "label": "Assistant Technical Director",
        "role_type": RoleType.NON_EDITOR_EXEC,
        "code": "J7M1-R8T5-K2P6"
    },
    "assistantSocialDirector": {
        "label": "Assistant Social Director",
        "role_type": RoleType.NON_EDITOR_EXEC,
        "code": "L4N3-B5Q9-H1V7"
    },
    "financialOfficer": {
        "label": "Financial Officer",
        "role_type": RoleType.EDITING_EXEC,
        "code": "W7U0-R5Z2-K9B8"
    },
    "assistantFinancialOfficer": {
        "label": "Assistant Financial Officer",
        "role_type": RoleType.NON_EDITOR_EXEC,
        "code": "X6V8-G7Q2-M5M1"
    },
    "pro_1": {
        "label": "Public Relations Officer 1",
        "role_type": RoleType.EDITING_EXEC,
        "code": "P8C2-K6M4-T1J9"
    },
    "pro_2": {
        "label": "Public Relations Officer 2",
        "role_type": RoleType.EDITING_EXEC,
        "code": "N8B4-J6M2-V3P5"
    },
    "pro_3": {
        "label": "Public Relations Officer 3",
        "role_type": RoleType.EDITING_EXEC,
        "code": "L3V7-H5C2-K9T1"
    },
    "pro_4": {
        "label": "Public Relations Officer 4",
        "role_type": RoleType.EDITING_EXEC,
        "code": "J1F6-P9R3-Q4M8"
    },
    "pro_5": {
        "label": "Public Relations Officer 5",
        "role_type": RoleType.EDITING_EXEC,
        "code": "T4M8-L2K5-B7F1"
    },
    "outgoneAdvisor1": {
        "label": "Intermediary to Seniors 1",
        "role_type": RoleType.EDITING_EXEC,
        "code": "V2C9-H6Q3-N1R7"
    },
    "outgoneAdvisor2": {
        "label": "Intermediary to Seniors 2",
        "role_type": RoleType.EDITING_EXEC,
        "code": "R9P2-M4L1-T5C3"
    }
}
