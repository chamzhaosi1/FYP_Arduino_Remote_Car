import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment as env} from 'src/environments/environment.prod';

@Injectable({
  providedIn: 'root'
})
export class IntrusionService {

  constructor(private http: HttpClient) { }

  uploadIntrImg(path:string, img_info:any){
    let fullUrl: string = env.http.apiUrl + path + "/";
    return this.http.post(fullUrl, img_info, { withCredentials: true, observe: 'response'})
  }

  updateIntrImg(path:string, img_info:any){
    let fullUrl: string = env.http.apiUrl + path + "/";
    return this.http.put(fullUrl, img_info, { withCredentials: true, observe: 'response'})
  }

  getIntrImg(path:string){
    let fullUrl: string = env.http.apiUrl + path + "/";
    return this.http.get(fullUrl, {withCredentials: true})
  }

  deleteIntrImg(path:string, id:number){
    let fullUrl: string = env.http.apiUrl + path + "/" +id;
    return this.http.delete(fullUrl, {withCredentials: true, observe: 'response'})
  }
}

