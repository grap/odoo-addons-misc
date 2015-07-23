## -*- coding: utf-8 -*-
<!DOCTYPE html SYSTEM "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
    <meta http-equiv="Content-Type" content="application/xhtml+xml;charset=utf-8" />
        <style type="text/css">
            body{
                padding:0px;margin:0px;border:0px;overflow:hidden;
            }
            div{
                padding:0px;margin:0px;border:0px;overflow:hidden;
            }
            .label_container{
                page-break-inside: avoid;
                width:7.0cm; height:4cm; float:left;
                background-color:green;
                border:1px solid;
            }
            .barcode_container{
            background-color:yellow;width:7.6cm; height:5.2cm;
            position:absolute;
            border:1px solid;
            }
            .ean13_image{
                margin: 0.5cm;
                width: 6.6cm;
                height: 4.2cm;
            }
            
        </style>
    </head>
    <body>

    %for wizard in objects:
    <!-- ligne 1 -->
    <div class="barcode_container" style="top:2.3cm;left:1.2cm;">
        <img class="ean13_image" src="data:image/png;base64,${wizard.product_id.ean13_image}"/>
    </div>
    <div class="barcode_container" style="top:2.3cm;left:9.1cm;">
        <img class="ean13_image" src="data:image/png;base64,${wizard.product_id.ean13_image}"/>
    </div>
    <div class="barcode_container" style="top:2.3cm;left:17.0cm;">
        <img class="ean13_image" src="data:image/png;base64,${wizard.product_id.ean13_image}"/>
    </div>
    <!-- ligne 2 -->
    <div class="barcode_container" style="top:7.7cm;left:1.2cm;">
        <img class="ean13_image" src="data:image/png;base64,${wizard.product_id.ean13_image}"/>
    </div>
    <div class="barcode_container" style="top:7.7cm;left:9.1cm;">
        <img class="ean13_image" src="data:image/png;base64,${wizard.product_id.ean13_image}"/>
    </div>
    <div class="barcode_container" style="top:7.7cm;left:17.0cm;">
        <img class="ean13_image" src="data:image/png;base64,${wizard.product_id.ean13_image}"/>
    </div>
    <!-- ligne 3 -->
    <div class="barcode_container" style="top:13.1cm;left:1.2cm;">
        <img class="ean13_image" src="data:image/png;base64,${wizard.product_id.ean13_image}"/>
    </div>
    <div class="barcode_container" style="top:13.1cm;left:9.1cm;">
        <img class="ean13_image" src="data:image/png;base64,${wizard.product_id.ean13_image}"/>
    </div>
    <div class="barcode_container" style="top:13.1cm;left:17.0cm;">
        <img class="ean13_image" src="data:image/png;base64,${wizard.product_id.ean13_image}"/>
    </div>
    <!-- ligne 4 -->
    <div class="barcode_container" style="top:18.5cm;left:1.2cm;">
        <img class="ean13_image" src="data:image/png;base64,${wizard.product_id.ean13_image}"/>
    </div>
    <div class="barcode_container" style="top:18.5cm;left:9.1cm;">
        <img class="ean13_image" src="data:image/png;base64,${wizard.product_id.ean13_image}"/>
    </div>
    <div class="barcode_container" style="top:18.5cm;left:17.0cm;">
        <img class="ean13_image" src="data:image/png;base64,${wizard.product_id.ean13_image}"/>
    </div>
    <!-- ligne 5 -->
    <div class="barcode_container" style="top:23.9cm;left:1.2cm;">
        <img class="ean13_image" src="data:image/png;base64,${wizard.product_id.ean13_image}"/>
    </div>
    <div class="barcode_container" style="top:23.9cm;left:9.1cm;">
        <img class="ean13_image" src="data:image/png;base64,${wizard.product_id.ean13_image}"/>
    </div>
    <div class="barcode_container" style="top:23.9cm;left:17.0cm;">
        <img class="ean13_image" src="data:image/png;base64,${wizard.product_id.ean13_image}"/>
    </div>
    <!-- ligne 6 -->
    <div class="barcode_container" style="top:29.3cm;left:1.2cm;">
        <img class="ean13_image" src="data:image/png;base64,${wizard.product_id.ean13_image}"/>
    </div>
    <div class="barcode_container" style="top:29.3cm;left:9.1cm;">
        <img class="ean13_image" src="data:image/png;base64,${wizard.product_id.ean13_image}"/>
    </div>
    <div class="barcode_container" style="top:29.3cm;left:17.0cm;">
        <img class="ean13_image" src="data:image/png;base64,${wizard.product_id.ean13_image}"/>
    </div>
        %for i in range(0, -1):
        %endfor

    %endfor
    </body>
</html>


