#!/bin/bash

jb build dart --builder pdfhtml && jb build dart;

cd dart && export_dir="export";
rm -r $export_dir/*;
mv _build/html $export_dir/html;
mv _build/pdf/book.pdf $export_dir/report.pdf;