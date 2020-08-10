import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent implements OnInit {
  baseUrl = 'http://localhost:5000';
  records = '/records';
  download = '/download';
  currentFilename: string = 'No File Selected';

  currentFile: File = null;
  fileList: string[] = [];
  viewFile: string[] = [];
  dateStat: number = 0;

  uploading = false;
  errorUploading = false;
  fetching = false;
  errorFetching = false;
  fetchingOne = false;
  errorFetchingOne = false;

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

    this.errorUploading = false;
    this.uploading = true;

    let formData: FormData = new FormData();
    formData.append('csvFile', this.currentFile, this.currentFile.name);

    await this.http.post(this.baseUrl + this.records, formData)
      .toPromise()
      .then(() => this.getAll())
      .catch(() => this.errorUploading = true)
      .finally(() => this.uploading = false);
  }

  public async getAll(): Promise<void> {
    this.errorFetching = false;
    this.fetching = true;

    await this.http.get(this.baseUrl + this.records).toPromise()
      .then((res: string[]) => this.fileList = res)
      .catch(() => this.errorFetching = true)
      .finally(() => this.fetching = false);
  }

  public onDownload(name) {
    const url = this.baseUrl + this.download + `\/${name}`;
    let downloadLink = window.document.createElement('a');
    downloadLink.href = url;
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
  }

  public async viewRecord(name): Promise<void> {
    this.errorFetchingOne = false;
    this.fetchingOne = true;
    this.currentFilename = name;

    const url = this.baseUrl + this.records + `\/${name}`;

    await this.http.get(url).toPromise()
      .then((res: string[]) => this.viewFile = res)
      .then(() => this.updateDateStat(name))
      .catch(() => this.errorFetchingOne = true)
      .finally(() => this.fetchingOne = false);
  }

  public async updateDateStat(name): Promise<void> {
    const url = this.baseUrl + this.records + `\/year\/${name}`;

    await this.http.get(url).toPromise()
      .then((res: number) => this.dateStat = res)
      .catch(() => this.errorFetchingOne = true)
      .finally(() => this.fetchingOne = false);
  }
}
