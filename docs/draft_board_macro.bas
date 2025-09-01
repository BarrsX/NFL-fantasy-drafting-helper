Private Sub Worksheet_Change(ByVal Target As Range)
    On Error Resume Next

    ' Only process changes in the Drafted column (Column I = 9)
    If Target.Column = 9 Then
        Application.EnableEvents = False

        If LCase(Trim(Target.Value)) = "x" Then
            ' Apply strikethrough to the entire row (A-H)
            With Target.EntireRow.Range("A1:H1")
                .Font.Strikethrough = True
                .Font.Color = RGB(128, 128, 128)
            End With
        ElseIf Target.Value = "" Then
            ' Remove strikethrough when X is cleared
            With Target.EntireRow.Range("A1:H1")
                .Font.Strikethrough = False
                .Font.Color = RGB(0, 0, 0)
            End With
        End If

        Application.EnableEvents = True
    End If
End Sub
