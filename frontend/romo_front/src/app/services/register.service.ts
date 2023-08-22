import { Injectable } from '@angular/core';
import { HttpClient  } from '@angular/common/http';
import { User } from '../interfaces/user'
import { environment as env} from 'src/environments/environment.prod';

@Injectable({
  providedIn: 'root'
})
export class RegisterService {

  constructor(private http : HttpClient) { }

  postRegister(path:string, user:User){
    let fullUrl:string = env.http.apiUrl + path  + "/";
    return this.http.post(fullUrl, user, {withCredentials: true,  observe: 'response'})
  }


}
