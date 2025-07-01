import {Component, OnInit} from '@angular/core';
import {TokenStorageService} from '../service/token-storage.service';
import {MatDialog} from '@angular/material/dialog';
import {AddStockDialogComponent} from '../add-stock-dialog/add-stock-dialog.component';
import {Router} from '@angular/router';
import {MatTableDataSource} from '@angular/material/table';
import {StockDataService} from '../service/stock-data.service';
import {CompanyDetailDialogComponent} from '../company-detail-dialog/company-detail-dialog.component';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  public username: string;
  value = '';
  error = '';
  displayedColumns: string[] = ['Symbol', 'Price', 'PurchasePrice', 'Amount', 'ChangePercent', 'PurchaseDate', 'SMA', 'MACD', 'RSI', 'Open', 'High', 'Low', 'Volume', 'CompanyDetails', 'Action'];
  dataSource: any[] = [];

  constructor(private tokenStorageService: TokenStorageService, private router: Router, private stockDataService: StockDataService,
              public dialog: MatDialog) {
  }

  ngOnInit(): void {
    this.username = this.tokenStorageService.getUser();
    this.loadUserPortfolio();
  }

  loadUserPortfolio() {
    this.stockDataService.getPortFolio().subscribe(
      data => {
        console.log(data);
        this.dataSource = data;
        if (this.dataSource.length === 0) {
          this.error = 'No results found';
        }
      },
      err => {
        console.log(err);
        this.error = 'Failed to fetch user portfolio';
      }
    );
  }

  searchStock() {
    this.router.navigate(['/search']);
  }

  viewCompanyDetail(symbol) {
    const dialogRef = this.dialog.open(CompanyDetailDialogComponent, {
      data: symbol
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log(`Dialog result: ${result}`);
    });
  }

  deleteStock(symbol) {
    this.stockDataService.deleteStock(symbol).subscribe(
      data => {
        console.log(data);
        this.loadUserPortfolio();
      },
      err => {
        console.log(err);
        this.loadUserPortfolio();
      }
    );
  }

}
