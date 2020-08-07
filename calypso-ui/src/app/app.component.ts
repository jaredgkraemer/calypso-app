import { Component } from '@angular/core';
import { Observable } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent {
  title = 'calypso-ui';
  url = 'http://localhost:5000/csv';
  currentFile: File = null;

  constructor(private http: HttpClient) {}

  onFileChange(event) {
    // let reader = new FileReader();
    // if (event.target.files && event.target.files.length > 0) {
    //   let file = event.target.files[0];
    //   reader.readAsDataURL(file);
    //   reader.onload = () => {
    //     console.log("TEST: ", reader.result);
    //   };
    // }
    // }
    if (event.target.files && event.target.files.length > 0) {
      this.currentFile = event.target.files[0];
      console.log('CURR FILE: ', this.currentFile);
    }
  }

  onUpload() {
    if (this.currentFile === null) return;

    console.log('UPLOAD');
    let formData: FormData = new FormData();

    formData.append('uploadFile', this.currentFile, this.currentFile.name);

    console.log('FORM DATA: ', formData);

    let headers = new HttpHeaders();
    headers.set('Content-Type', 'multipart/form-data');

    let options = { headers: headers };

    console.log('HEADERS: ', headers)

    let test = {
      name: this.currentFile.name,
      data: this.currentFile
    }

    this.http.post(this.url, test, options)
      .subscribe(
        (data) => console.log('SUCCESS: ', data),
        (error) => console.log('ERROR: ', error)
      );
  }

  onGet() {
    this.http.get(this.url)
      .subscribe(
        (data) => console.log('SUCCESS: ', data),
        (error) => console.log('ERROR: ', error)
      );
  }
}
