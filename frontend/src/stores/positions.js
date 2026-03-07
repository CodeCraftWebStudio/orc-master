import { forEach } from "mathjs";

function makePosition(position_name, position_type, position_code ) {
    return {
        name: position_name,
        type: position_type,
        code: position_code
    }
} 

export async function GetCodes(position, base='http://localhost:5000') {

    const magicKeyRoute = '/api/user/getMagicKey';
    const magicKeyConfig = {
        method: 'POST',
        credentials: 'include',
        headers: {'Content-Type': 'application/json'},
        body: {
            'session_key': localStorage.getItem('session')
        }
    }
    const magicKeyResponse = await (await fetch(`${base}${magicKeyRoute}`, magicKeyConfig)).json();
    const hashRoute = '/api/tools/getHashedValue';
    const hashedKeyConfig = {
        value: magicKeyResponse,
    }
    const codeRouteName = '/api/user/getUserCodes';
    const codeRouteConfig = {
        passcode: await (await fetch(`${base}${hashRoute}`, hashedKeyConfig)).json(),
        session_key: localStorage.getItem('key'),
        position_name: position
    }
    let isDisabled;
    let theFinalResult = await (await fetch(`${base}${codeRouteName}`, codeRouteConfig)).json();
    localStorage.setItem('key', theFinalResult.session_key);
    if (theFinalResult.disabled_roles && theFinalResult.diabled_roles.length && theFinalResult.disabled_roles.includes(position)) {
       isDisabled = true; 
    } else {
        isDisabled = false;
    }
    return {code: theFinalResult.position_code, disabled: isDisabled}
}



export const position_types = {
    admin: 'ADMIN',
    edit: 'EDITING_EXECUTIVE',
    nonEdit: 'NON_EDITING_EXECUTIVE',
    member: 'MEMBER',
    guest: 'GUEST,'
}
export const position_names = {
    president: 'President',
    vicePresident: 'Vice President',
    commandant: 'Parade Commandant',
    assistantCommandant: 'Assistant Commandant',
    secretary: 'General Secreatary',
    assistantSecretary: 'Assistant General Secretary',
    socialDirector: 'Social Director',
    technicalDirector: 'Technical Director',
    assistantTechnicalDirector: 'Assistant Technical Director',
    assistantSocialDirector: 'Assistant Social Director',
    financialOfficer: 'Financial Officer',
    assistantFinancialOfficer: 'Assistant Financial Officer',
    pro_1: 'Public Relations Officer 1',
    pro_2: 'Public Relations Officer 2',
    pro_3: 'Public Relations Officer 3',
    pro_4: 'Public Relations Officer 4',
    pro_5: 'Public Relations Officer 5',
    outgoneAdvisor1: 'Intemediary to Seniors 1',
    outgoneAdvisor2: 'Intemediary to Seniors 2',
}
export const position_codes = {
    president: 'A1K9-M3T6-Q2V8',
    vicePresident: 'D4F7-L1P9-C8J2',
    commandant: 'M5B2-H8N1-K3Q7',
    assistantCommandant: 'E3X7-V1Q4-K6J8',
    secretary: 'R6P4-T2J9-L1C8',
    assistantSecretary: 'K5J1-P7M4-L8V2',
    socialDirector: 'V9K1-Q3M7-P5B2',
    technicalDirector: 'C2H6-F9L4-N3V8',
    assistantTechnicalDirector: 'J7M1-R8T5-K2P6',
    assistantSocialDirector: 'L4N3-B5Q9-H1V7',
    financialOfficer: 'W7U0-R5Z2-K9B8',
    assistantFinancialOfficer: 'X6V8-G7Q2-M5M1',
    pro_1: 'P8C2-K6M4-T1J9',
    pro_2: 'N8B4-J6M2-V3P5',
    pro_3: 'L3V7-H5C2-K9T1',
    pro_4: 'J1F6-P9R3-Q4M8',
    pro_5: 'T4M8-L2K5-B7F1',
    outgoneAdvisor1: 'V2C9-H6Q3-N1R7',
    outgoneAdvisor2: 'R9P2-M4L1-T5C3',
}

console.log("Position Names type", typeof(position_names));
let codes = {};

const position_keys = position_names.keys;
console.log("Position keys", position_keys);
for (let i of position_keys) {
    codes.i = await GetCodes();
}
// Red Cross Positions in Order of Hierachy, PROs, though of a lower rank, possess editing allowance due to the nature of their work
export const positions = [
    makePosition(position_names.president, position_types.admin, position_codes.president),
    makePosition(position_names.vicePresident, position_types.edit, position_codes.vicePresident),
    makePosition(position_names.commandant, position_types.edit, position_codes.commandant),
    makePosition(position_names.secretary, position_types.edit, position_codes.secretary),
    makePosition(position_names.financialOfficer, position_types.financialOfficer, position_codes.financialOfficer),
    makePosition(position_names.technicalDirector, position_types.nonEdit, position_codes.technicalDirector),
    makePosition(position_names.socialDirector, position_types.nonEdit, position_codes.socialDirector),
    makePosition(position_names.assistantCommandant, position_types.nonEdit, position_codes.assistantCommandant),
    makePosition(position_names.assistantSecretary, position_types.nonEdit, position_codes.assistantSecretary),
    makePosition(position_names.assistantFinancialOfficer, position_types.nonEdit, position_codes.assistantFinancialOfficer),
    makePosition(position_names.assistantTechnicalDirector, position_types.nonEdit, position_codes.assistantTechnicalDirector),
    makePosition(position_names.assistantSocialDirector, position_types.nonEdit, position_codes.assistantSocialDirector),
    makePosition(position_names.pro_1, position_types.edit, position_codes.pro_1),
    makePosition(position_names.pro_2, position_types.edit, position_codes.pro_2),
    makePosition(position_names.pro_3, position_types.edit, position_codes.pro_3),
    makePosition(position_names.pro_4, position_types.edit, position_codes.pro_4),
    makePosition(position_names.pro_5, position_types.edit, position_codes.pro_5),
    makePosition(position_names.outgoneAdvisor1, position_types.edit, position_codes.outgoneAdvisor1),
    makePosition(position_names.outgoneAdvisor2, position_types.edit, position_codes.outgoneAdvisor2),
]
