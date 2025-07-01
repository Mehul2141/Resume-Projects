import {Component, Input, OnInit} from '@angular/core';
import {AddStockDialogComponent} from '../add-stock-dialog/add-stock-dialog.component';
import {MatDialog} from '@angular/material/dialog';

@Component({
  selector: 'app-search-result-card',
  templateUrl: './search-result-card.component.html',
  styleUrls: ['./search-result-card.component.css']
})
export class SearchResultCardComponent implements OnInit {
  @Input() result!: any;

  constructor(public dialog: MatDialog) { }

  ngOnInit(): void {
  }

  openDialog() {
    const dialogRef = this.dialog.open(AddStockDialogComponent, {
      data: this.result
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log(`Dialog result: ${result}`);
    });
  }
}
