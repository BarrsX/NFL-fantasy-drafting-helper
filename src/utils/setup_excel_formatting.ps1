# PowerShell script to automatically set up conditional formatting in Excel
# This script will open Excel, apply conditional formatting, and save the file

param(
    [string]$ExcelFile = "output\dynasty_superflex_cheatsheet.xlsx",
    [string]$OutputFile = ""  # Leave empty to save in place
)

Write-Host "Setting up automatic strikethrough formatting in Excel..." -ForegroundColor Green

try {
    # Create Excel application object
    $excel = New-Object -ComObject Excel.Application
    $excel.Visible = $false
    $excel.DisplayAlerts = $false

    # Open the workbook
    $workbook = $excel.Workbooks.Open((Resolve-Path $ExcelFile).Path)
    $worksheet = $workbook.Sheets.Item("Draft Board")

    Write-Host "Opened Excel file and Draft Board sheet" -ForegroundColor Yellow

    # Get the used range
    $usedRange = $worksheet.UsedRange
    $lastRow = $usedRange.Rows.Count

    Write-Host "Found $lastRow rows of data" -ForegroundColor Yellow

    # Select columns A:H for conditional formatting
    $rangeString = "A2:H$lastRow"
    $range = $worksheet.Range($rangeString)

    Write-Host "Applying conditional formatting to range: $rangeString" -ForegroundColor Yellow

    # Add conditional formatting rule
    $conditionalFormat = $range.FormatConditions.Add(2, 0, '=$I2="X"', $range)  # xlExpression = 2

    # Set the formatting (strikethrough and gray text)
    $conditionalFormat.Font.Strikethrough = $true
    $conditionalFormat.Font.Color = 8421504  # Gray color

    Write-Host "Conditional formatting rule applied successfully!" -ForegroundColor Green

    # Save the workbook
    if ($OutputFile -eq "") {
        # Save in place
        $workbook.Save()
        Write-Host "File saved in place" -ForegroundColor Green
    } else {
        # Save to new location
        try {
            $outputPath = Resolve-Path $OutputFile -ErrorAction Stop
            $workbook.SaveAs($outputPath.Path)
            Write-Host "File saved as: $OutputFile" -ForegroundColor Green
        } catch {
            # If output path doesn't exist, save in place
            $workbook.Save()
            Write-Host "Output path not found, saved in place instead" -ForegroundColor Yellow
        }
    }
    Write-Host "" -ForegroundColor White
    Write-Host "SUCCESS! Your Excel file now has automatic strikethrough formatting." -ForegroundColor Green
    Write-Host "Just type 'X' in the Drafted column (I) and the row will be crossed out automatically!" -ForegroundColor White
    Write-Host "The formatting has been applied to your original file." -ForegroundColor Cyan

} catch {
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Make sure Excel is installed and the file path is correct." -ForegroundColor Red
} finally {
    # Clean up
    if ($workbook) { $workbook.Close($false) }
    if ($excel) { $excel.Quit() }

    # Release COM objects
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($worksheet) | Out-Null
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($workbook) | Out-Null
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($excel) | Out-Null
    [System.GC]::Collect()
    [System.GC]::WaitForPendingFinalizers()
}

Write-Host "Script completed." -ForegroundColor Cyan
