import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ROMO } from '../interfaces/romo'
import { environment as env} from 'src/environments/environment.prod';

@Injectable({
  providedIn: 'root'
})
export class RomoService {

  constructor(private http: HttpClient) { }

  getRomoDetail(path:string){
    let fullUrl: string = env.http.apiUrl + path + "/";
    return this.http.get(fullUrl, { withCredentials: true, observe: 'response'})
  }

  getRomoUser(path:string, mac_address:string){
    let fullUrl: string = env.http.apiUrl + path + "/" + mac_address;
    return this.http.get(fullUrl, { withCredentials: true, observe: 'response'})
  }

  romoRegister(path:string, romo_info:ROMO){
    let fullUrl: string = env.http.apiUrl + path + "/";
    return this.http.post(fullUrl, romo_info, { withCredentials: true, observe: 'response'})
  }

  deleteRomo(path:string, mac_address:string){
    let fullUrl: string = env.http.apiUrl + path + "/" +mac_address;
    return this.http.delete(fullUrl, {withCredentials: true, observe: 'response'})
  }

  romoUpdate(path:string, romo_info:ROMO){
    let fullUrl: string = env.http.apiUrl + path + "/";
    return this.http.put(fullUrl, romo_info, { withCredentials: true, observe: 'response'})
  }
}
