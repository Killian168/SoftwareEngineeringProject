import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})

export class UserService {

  Url:string = 'https://b9slmu5q90.execute-api.eu-west-1.amazonaws.com/prod';
  createAcc:string = '/createaccount';

  constructor(private http:HttpClient) {}

  storeAccountDetails(userDets:any) {
    this.http.post<any>((this.Url+this.createAcc), userDets).subscribe(
      data => {return data},
      err => {return err}
    );
  }


}