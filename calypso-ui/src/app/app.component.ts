import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent implements OnInit {
  url = 'http://localhost:5000/records';
  currentFile: File = null;
  fileList: string[] = [];
  uploading = false;
  errorUploading = false;
  fetching = false;
  errorFetching = false;

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.getAll();
  }

  public onFileChange(files: FileList) {
    if (files && files.length > 0) {
      this.currentFile = files[0];
    }
  }

  public async onUpload(): Promise<void> {
    if (this.currentFile === null) return;

    this.getAll();

    if (this.fileList.includes(this.currentFile.name)) return;

    this.errorUploading = false;
    this.uploading = true;

    let formData: FormData = new FormData();
    formData.append('csvFile', this.currentFile, this.currentFile.name);
    
    await this.http.post(this.url, formData)
      .toPromise()
      .then((data: any) => this.fileList.push(data.filename))
      .catch(() => this.errorUploading = true)
      .finally(() => this.uploading = false);
  }

  public async getAll(): Promise<void> {
    this.errorFetching = false;
    this.fetching = true;

    await this.http.get(this.url).toPromise()
      .then((data: string[]) => this.fileList = data)
      .catch(() => this.errorFetching = true)
      .finally(() => this.fetching = false);
  }
}
