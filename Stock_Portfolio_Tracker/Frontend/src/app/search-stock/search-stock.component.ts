import {Component, OnInit} from '@angular/core';
import {AddStockDialogComponent} from '../add-stock-dialog/add-stock-dialog.component';
import {MatDialog} from '@angular/material/dialog';
import {StockDataService} from '../service/stock-data.service';
import {Router} from '@angular/router';

@Component({
  selector: 'app-search-stock',
  templateUrl: './search-stock.component.html',
  styleUrls: ['./search-stock.component.css']
})
export class SearchStockComponent implements OnInit {
  searchQuery = '';
  searchResults: any;
  error = '';

  constructor(private stockDataService: StockDataService, private router: Router) {
  }

  ngOnInit(): void {
  }

  // tslint:disable-next-line:typedef
  searchStocks() {
    if (this.searchQuery) {
      this.error = null;
      this.stockDataService.searchStocks(this.searchQuery).subscribe(
        data => {
          console.log(data);
          this.searchResults = data;
          if (this.searchResults.length === 0) {
            this.error = 'No results found';
          }
        },
        err => {
          console.log(err);
          this.error = 'Failed to search stocks';
        }
      );
    }
  }

  portfolio() {
    this.router.navigate(['/home']);
  }

}
