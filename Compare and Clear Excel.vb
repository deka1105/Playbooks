Sub ClearAll()
    Dim subI As Integer
    Dim subJ As Integer
    Dim count As Integer
    
    subI = 2
    subJ = 2

    With Worksheets("Sheet1")
        With .Cells(2, 2).CurrentRegion
            With .Resize(.Rows.count, .Columns.count).Offset(1, 1)
                .Cells.Interior.Pattern = xlNone
            End With
        End With
    End With

    
End Sub

Sub RunCompare()

    Dim res As Integer
    Dim total As Integer
    
    Dim subI As Integer
    Dim subJ As Integer
    Dim ansI As Integer
    Dim ansJ As Integer
    Dim count As Integer
    
    Dim sVal As String
    Dim aVal As String
    
    count = 14 'Number of Columns in the Excel sheets
    total = 0
    res = 0
    ansI = 2
    ansJ = 2
    
    subI = 2
    subJ = 2

    For i = 0 To count - 1
        For j = 0 To count - 1
            sVal = ThisWorkbook.Worksheets("Sheet1").Cells(subI + i, subJ + j).Value
            aVal = ThisWorkbook.Worksheets("Answers").Cells(ansI + i, ansJ + j).Value
            If aVal = "X" Then
                total = total + 1
                If (sVal = "1") And (aVal = "X") Then
                    ThisWorkbook.Worksheets("Sheet1").Cells(subI + i, subJ + j).Interior.Color = vbGreen
                    res = res + 1
                Else
                    ThisWorkbook.Worksheets("Sheet1").Cells(subI + i, subJ + j).Interior.Color = vbRed
                End If
            ElseIf sVal <> aVal Then
                ThisWorkbook.Worksheets("Sheet1").Cells(subI + i, subJ + j).Interior.Color = vbYellow
            End If
        Next j
    Next i
MsgBox "Result : " & res & "/" & total, vbInformation
End Sub
