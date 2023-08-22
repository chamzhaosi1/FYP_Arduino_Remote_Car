import { Injectable, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { User } from '../interfaces/user'
import { environment as env} from 'src/environments/environment.prod';

@Injectable({
  providedIn: 'root'
})
export class UsersService implements OnInit {

  constructor(private http: HttpClient) {}

  ngOnInit() { }

  postLogin(path: string, user: User) {
    let fullUrl: string = env.http.apiUrl + path + "/";
    // three parameter will get HTTPResponse data type, and only this kind of data type can update cookies
    return this.http.post(fullUrl, user, { withCredentials: true, observe: 'response' })
  }

  getAutheToken(path: string) {
    let fullUrl: string = env.http.apiUrl + path + "/";
    return this.http.get(fullUrl, { withCredentials: true, observe: 'response' })
  }

  postLogout(path: string) {
    let fullUrl: string = env.http.apiUrl + path + "/";
    // three parameter will get HTTPResponse data type, and only this kind of data type can update cookies
    // so event the body is empty, we still need to pass it
    return this.http.post(fullUrl, {}, { withCredentials: true, observe: 'response' })
  }

  postRegister(path: string, user: User) {
    let fullUrl: string = env.http.apiUrl + path + "/";
    return this.http.post(fullUrl, user, { withCredentials: true, observe: 'response' })
  }

}
