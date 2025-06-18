<?php
$uri =  $_SERVER['REQUEST_URI'];
$method =  $_SERVER['REQUEST_METHOD'];

// $body = json_decode(file_get_contents('php://input'));

if ($method == 'GET') {
    http_response_code(405);
    echo "GET method not allowed";
    exit();
}


function get_stock(){
    // $min = -10;
    // $max = rand(10, 100);

    $min = 2;
    $max = rand(5, 50);

    $STOCK = [
        'NUOC-HOA-CN-001' => 1, 
		'NUOC-HOA-DIOR-002' => 1,
		'NUOC-HOA-LL-003' => 1, 
		'NUOC-HOA-LC-004' => 1, 
		'NUOC-HOA-CR-005' => 1,
		'NUOC-HOA-BY-006' => 1,
		'SUA-TAM-DV-001' => 1, 
		'SUA-TAM-PP-002' => 1, 
		'SUA-TAM-LB-003' => 0, 
		'SUA-TAM-CT-004' => 0, 
		'SUA-TAM-CC-005' => 1, 
		'SUA-TAM-TD-006' => 1, 
		'TINH-DAU-KD-001' => 1, 
		'TINH-DAU-SB-002' => 1, 
		'TINH-DAU-GG-003' => 1, 
		'TINH-DAU-OC-004' => 1, 
		'TINH-DAU-EA-005' => 1, 
		'TINH-DAU-RE-006' => 1, 
		'DAU-GOI-PT-001' => 1, 
		'DAU-GOI-TR-002' => 1, 
		'DAU-GOI-CM-003' => 0, 
		'DAU-GOI-NX-004' => 1, 
		'DAU-GOI-SL-005' => 1, 
		'DAU-GOI-BC-006' => 0, 
		'XA-PHONG-TX-001' => 1, 
		'XA-PHONG-TH-002' => 1, 
		'XA-PHONG-HC-003' => 1, 
		'XA-PHONG-MO-004' => 1, 
		'XA-PHONG-NA-005' => 1, 
		'XA-PHONG-CG-006' => 1, 
		'SUA-RUA-MT-CE-001' => 0, 
		'SUA-RUA-MT-SK-002' => 1, 
		'SUA-RUA-MT-CX-003' => 1, 
		'SUA-RUA-MT-IF-004' => 1, 
		'SUA-RUA-MT-KL-005' => 0, 
		'SUA-RUA-MT-LP-006' => 1
    ];

    foreach ($STOCK as $key => $value) {
		if ($value > 0) {
			$STOCK[$key] = rand($min, $max);
		}
    }

    return $STOCK;
}

function check_stock(){
    $STOCK = get_stock();
    $body = json_decode(file_get_contents('php://input'), true);

    $order_items = $body['order_items'];
	
    $result = [];
    $as_least_out_stock = false;
    foreach ($order_items as $item) {
        $sku = $item['sku'];
        $qty_ordered = $item['ordered_qty'];
        $stock_status = 'IN_STOCK';

        if ($STOCK[$sku] == 0){
            $stock_status = 'OUT_STOCK';
            $as_least_out_stock = true;
        }
        elseif($STOCK[$sku] < $qty_ordered){
            $stock_status = 'NOT_ENOUGH_QUANTITY';
            $as_least_out_stock = true;
        }
        else{
            $stock_status = 'IN_STOCK';
            
        }

        $result[] = [
            'sku' => $sku,
            'ordered_qty' => $qty_ordered,
            'stock_qty' => $STOCK[$sku],
            'status' => $stock_status
        ];

    }
       
    return ['data' => $result];
}

header('Content-Type: application/json; charset=utf-8');
echo json_encode(check_stock());