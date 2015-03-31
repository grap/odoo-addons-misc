## -*- coding: utf-8 -*-
<!DOCTYPE html SYSTEM "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
    <meta http-equiv="Content-Type" content="application/xhtml+xml;charset=utf-8" />
        <style type="text/css">
        .root_category{
            background-color: #CC9;
        }
        .middle_category{
            background-color: #DDA;
        }
        .final_category{
            background-color: #EEC;
        }
        .inactive_product{
            font-style: italic;
        }
        .null_valuation{
            color: #DDD;
        }
        .currency{
            text-align: right;
        }
        </style>
    </head>
    <body>
    %for wizard in objects :
<%
        currency = wizard.company_id.currency_id.symbol
%>
    <table border="1" width="100%">
        <thead>
            <tr>
                <th colspan="2"><h>${_('Stock Valuation')}</h></th>
            </tr>
        </thead>
            <tr>
                <th>${_('Company')}</th>
                <td>${wizard.company_id.name}</td>
            </tr>
            <tr>
                <th>${_('Valuation Date')}</th>
                <td>${wizard.valuation_date}</td>
            </tr>
            <tr>
                <th>${_('Print Date')}</th>
                <td>${wizard.print_date}</td>
            </tr>
        %if len(wizard.inventory_ids) != 0:
            <tr>
                <th>${_('Inventory Variations')}</th>
                <td>
                    <ul>
            ${_('The following inventories, realized after the requested date, has been taken into account for the valuation, in the variation column.')}
            %for inventory in wizard.inventory_ids:
                        <li>${inventory.date} : ${inventory.name}</li>
            %endfor
                    </ul>
                </td>
            </tr>
        %endif
            <tr>
                <th>${_('Cost Method Description')}</th>
                <td>
                ${_('The cost price is the one defined at print date. (The software does not manage the history of cost price.)')}
                    <ul>
                ${_('The Method Column indicates how the cost price is defined by product.')}
                        <li>${_('M: Manual: The user fill the value manually;')}</li>
                        <li>${_('A: Automatic: The system generated a cost for the product, using one of the following valuation methods CUMP, LIFO, FIFO, LPP, NIFO...;')})</li>
                    </ul>
                </td>
            </tr>
            <tr>
                <th>${_('Total')}</th>
                <td>${wizard.total_valuation} ${currency}</td>
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
            %if category_line.total_valuation != 0:
                %if not category_line.category_id.parent_id:
        <tr class="root_category">
                %elif category_line.category_id.type == 'view':
        <tr class="middle_category">
                %else:
        <tr class="final_category">
                %endif

                %if len(category_line.wizard_id.inventory_ids) != 0:
            <td colspan="3">
                %else:
            <td colspan="1">
                %endif
                    ${category_line.category_id.complete_name}
            </td>
            <td colspan="3">${category_line.total_product_qty} ${_('Products')}</td>
            <td colspan="2" class="currency">${category_line.total_valuation} ${currency}</td>
        </tr>
<!-- For each Product -->
                %for product_line in category_line.product_line_ids:
<%
                    product_class = ''
%>
                    %if not product_line.product_id.active:
<%
                        product_class += ' inactive_product'
%>
                    %endif
                    %if product_line.valuation == 0:
<%
                        product_class += ' null_valuation'
%>
                    %endif
        <tr class="${product_class}">

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
            <td>${_('A')}</td>
                    %endif
            <td class="currency">${product_line.valuation} ${currency}</td>
        </tr>
                %endfor
            %endif
        %endfor
            
    </tbody>
</table>
    %endfor
    </body>
</html>


