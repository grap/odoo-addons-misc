## -*- coding: utf-8 -*-
<!DOCTYPE html SYSTEM "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
    <meta http-equiv="Content-Type" content="application/xhtml+xml;charset=utf-8" />
        <style type="text/css">

        </style>
    </head>
    <body>
    %for wizard in objects :
<table border="1" width="100%">
    <thead>
        <tr>
            <th>${_('Product')}</th>
            <th>&nbsp;</th>
            <th>${_('Confirmed Qty')}</th>
            <th>&nbsp;</th>
            <th>${_('Qty On Hand')}</th>
            <th>${_('Incoming Qty')}</th>
            <th>${_('Outgoing Qty')}</th>
        </tr>
    </thead>
    <tbody>
        %for line in wizard.line_ids:
        <tr>
            <td>${line.product_id.name}</td>
            <th>&nbsp;</th>
            <td><b>${line.confirmed_qty}</b></td>
            <td>&nbsp;</td>
            <td>${line.qty_available}</td>
            <td>+ ${line.incoming_qty}</td>
            <td>${line.outgoing_qty}</td>
        </tr>
        %endfor
    </thead>
</table>
    %endfor
    </body>
</html>


