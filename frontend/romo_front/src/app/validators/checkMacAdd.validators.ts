import {AbstractControl, ValidationErrors } from "@angular/forms";

export class checkMacAdd{

	static checkMacAddValidations(control: AbstractControl) : ValidationErrors | null{
	
		let controlValue = control.value as string;

		if(controlValue.split(":").length === 6){
            return null;	
		}else{
            return { checkMacAddValidations : true};	
		}
	}
}