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
            <th colspan="2">${_('Blablabla')}</th>
        </tr>
    </thead>
        <tr>
            <th>${_('Date')}</th>
            <td>${wizard.valuation_date}</td>
        </tr>
        %if len(wizard.inventory_ids) != 0:
        <tr>
            <th>${_('Inventory Variations')}</th>
            <td>
                <ul>
            ${_('The following inventories realized after the requested date has been taken into account for the valuation, in the variation column.')}
            %for inventory in wizard.inventory_ids:
                    <li>
                        {inventory.date} : {inventory.name}
                    </li>
            %endfor
                </ul>
            
            </td>
        </tr>
        %endif
        <tr>
            <th>${_('Cost Method Description')}</th>
            <td>
                <ul>
                ${_('The Method Column indicate how the cost price is defined by product')}
                    <li>${_('M : Manual : The user fill the value manually.')}</li>
                    <li>${_('C : Computed : The system generated a cost for the product, using one valuation method. (CUMP, LIFO, FIFO, LPP, NIFO...')})</li>
                </ul>
            </td>
        </tr>
        <tr>
            <th>${_('Total')}</th>
            <td>${wizard.total_valuation}</td>
        </tr>
    <tbody>
    </tbody>
</table>
    <table border="1" width="100%">
    <thead>
        <tr>
            <th>${_('Name')}</th>
            %if len(wizard.inventory_ids) != 0:
                <th>${_('Theoretical Qty')}</th>
                <th>${_('Variation')}</th>
            %endif
            <th>${_('Total Qty')}</th>
            <th>${_('UoM')}</th>
            <th>${_('Cost')}</th>
            <th>${_('Method')}</th>
            <th>${_('Total')}</th>
        </tr>
    </thead>
    <tbody>
<!-- For each Category -->
        %for category_line in wizard.category_line_ids:
        <tr>
            %if len(category_line.wizard_id.inventory_ids) != 0:
            <td colspan="7">
            %else:
            <td colspan="5">
            %endif
                ${category_line.category_id.complete_name}
            </td>
            <td>${category_line.valuation}</td>
        </tr>
<!-- For each Product -->
            %for product_line in category_line.product_line_ids:
        <tr>
            <td>${product_line.product_id.name}</td>
                %if len(category_line.wizard_id.inventory_ids) != 0:
                <td>${product_line.qty_available}</td>
                <td>${product_line.qty_variation}</td>
                %endif
            <td>${product_line.qty_total}</td>
            <td>${product_line.product_id.uom_id.name}</td>
            <td>${product_line.product_id.standard_price}</td>
            %if product_line.product_id.cost_method == 'standard':
            <td>${_('M')}</td>
            %else:
            <td>${_('C')}</td>
            %endif
            <td>${product_line.valuation}</td>
        </tr>
            %endfor
        %endfor
    </thead>
</table>
    %endfor
    </body>
</html>


