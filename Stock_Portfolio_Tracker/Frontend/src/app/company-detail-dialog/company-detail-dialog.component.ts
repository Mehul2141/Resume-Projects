import {Component, Inject, OnInit} from '@angular/core';
import {StockDataService} from '../service/stock-data.service';
import {MAT_DIALOG_DATA} from '@angular/material/dialog';

@Component({
  selector: 'app-company-detail-dialog',
  templateUrl: './company-detail-dialog.component.html',
  styleUrls: ['./company-detail-dialog.component.css']
})
export class CompanyDetailDialogComponent implements OnInit {
  error = null;
  data: any;

  constructor(@Inject(MAT_DIALOG_DATA) public symbol: { defaultValue: any }, private stockDateService: StockDataService) {
  }

  ngOnInit(): void {
    this.error = null;
    this.stockDateService.getCompanyDetails(this.symbol).subscribe(
      data => {
        console.log(data);
        this.data = data;
      },
      err => {
        console.log(err);
        this.error = 'Failed to fetch company details';
      }
    );
  }

}
