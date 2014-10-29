## -*- coding: utf-8 -*-
<!DOCTYPE html SYSTEM "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
    <meta http-equiv="Content-Type" content="application/xhtml+xml;charset=utf-8" />
        <style type="text/css">
            body{
                font-family: arial, verdana, sans-serif;
            }
            div{
                padding:0px;margin:0px;border:0px;overflow:hidden;
            }
            .label_container{
                page-break-inside: avoid;
                width:12.85cm; height:5.2cm; float:left;
            }
            .label_border{
                margin-left:1.15cm;
                margin-right:1.1cm;
                margin-top:0.35cm;
                margin-bottom:0.35cm;
                padding:0.15cm;
            }
            .label{
                width:10.3cm; height:4.2cm;
                }
            .label_left{
                width:6.7cm; height:4.2cm; float:left;
                }
            div.product_name{
                width:6.7cm; height:1.3cm;
                font-size:17px; font-weight:bold;
                }
            div.product_informations{
                background-color: rgba(255, 255, 255, 1);
                width:6.7cm;height:2.0cm;
                font-size:11px;
                }
            div.organic_text{
                width:4cm;height:1.0cm;
                font-weight:bold;
                font-size:11px;
                float:left;
            }
            div.product_labels{
                width:6.7cm; height:1cm;
                }
            img.product_label{
                width:0.8cm; height:0.8cm; margin:0.1cm;
                }
            div.label_right{
                width:3.6cm; height:4.2cm; float:left;
            }
            div.product_price{
                width:3.6cm; height:1.2cm;
                line-height: 1.2cm;
                text-align:center; font-size:22px; font-weight:bold;
                }
            div.product_image{
                width:3.1cm; height:3cm;
                }
            img.product_image{
                margin-left:0.05cm;
                width:3cm; height:3cm;
                }
        </style>
    </head>
    <body>
    %for wizard in objects :
        <!-- Empty labels -->
        %for i in range(0,wizard.offset):
        <div class="label_container">
        </div>
        %endfor

        <!-- Product labels -->
        %for line in wizard.line_ids:
            %for i in range(0,line.quantity):
        <div class="label_container">
                %if wizard.border:
                <div class="label_border" style="border: 1px solid;">
                %else:
                <div class="label_border">
                %endif
                    <div class="label">
                        <div class="label_left">
                            <div class="product_name" style="background-color:${line.product_id.pricetag_color};">
                            ${line.product_id.name}
                            </div>
                            <div class="product_informations" >
                %if line.product_id.code:
                                ${_('Code: ')}<b>${line.product_id.code}</b>
                %endif
                %if line.product_id.fresh_category:
                                &nbsp;-&nbsp;${_('Category: ')}<b>${line.product_id.fresh_category}</b>
                %endif
                                <br />
                %if line.product_id.volume:
                                ${_('Price Per Liter: ')}<b>${line.product_id.price_volume} &#128;</b>
                %elif line.product_id.weight_net:
                                ${_('Price Per Kilo: ')}<b>${line.product_id.price_weight_net} &#128;</b>
                %else:
                                ${_('Unit Price: ')}<b>${line.product_id.list_price} &#128;</b>
                %endif
                                <br />
                %if line.product_id.pricetag_origin:
                                ${_('Origin: ')}<b>${line.product_id.pricetag_origin}</b>
                                <br />
                %endif
                %if line.product_id.maker_description:
                                ${_('Maker: ')}<b>${line.product_id.maker_description}</b>
                %endif
                                <br />
                            </div>
                            <div class="product_labels">
                %for label in line.product_id.label_ids:
                                <img class="product_label" src="data:image/png;base64,${label.image}"/>
                %endfor
                %if line.product_id.pricetag_organic_text:
                                <div class="organic_text">${line.product_id.pricetag_organic_text}</div>
                %endif
                            </div>
                        </div>
                        <div class="label_right">
                            <div class="product_price" style="background-color:${line.product_id.pricetag_color};">
                %if line.print_unit_price:
                                ${line.product_id.list_price} &#128;
                %else:
                                &nbsp;&nbsp;&nbsp;&nbsp; &#128;
                %endif
                %if line.product_id.uom_id.category_id.pricetag_printable:
&nbsp;/&nbsp;${line.product_id.uom_id.name}
                %endif
                            </div>
                            <div class="product_image">
                %if wizard.radar_chart:
                                <img class="product_image" src="data:image/png;base64,${line.product_id.pricetag_image}"/>
                %else:
                                <img class="product_image" src="data:image/png;base64,${line.product_id.company_id.pricetag_image}"/>
                %endif
                            </div>
                        </div>
                    </div>
                </div>
        </div>
            %endfor
        %endfor
    %endfor
    </body>
</html>


