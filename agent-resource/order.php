<?php
$uri =  $_SERVER['REQUEST_URI'];
$method =  $_SERVER['REQUEST_METHOD'];

if ($method == 'GET') {
    http_response_code(405);
    echo "GET method not allowed";
    exit();
}

$body = json_decode(file_get_contents('php://input'), true);
// $url = "https://script.google.com/macros/s/AKfycbx_Q6kzNJzYJtEcPA-nuOmgvOcKwB0MfyU90ScbWbQWMsVCNGSsfP1BvdKTPMCx2NPilQ/exec";
$url = "https://script.google.com/macros/s/AKfycbxfxhGV1OZII_BMwQJtxNemjf5NMuMzLYUMb_A1HwfJ1Rc2G13Jw981kkUn9ccgcWF_Uw/exec";


function save_order($body, $url){
    $order = $body['order'];
    
    $payload = [
        "sheet_name" => "Orders",
        "data" => $order
    ];
    
    $headers = [
        // 'User-Agent' => 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1788.0',
        // 'Content-Type' => 'application/json',
        // 'Accept' => 'application/json'
    ];

    return call_api("POST", $url, $headers, json_encode($payload));
        
}

function save_order_items($body, $url){
    $items = $body['order_items'];
    $payload = [
        "sheet_name" => "Order_Items",
        "data" => $items
    ];

    $headers = [];

    return call_api("POST", $url, $headers, json_encode($payload));
}

function call_api($method, $url, $headers=[], $data = [])
{
    $curl = curl_init();

    switch ($method)
    {
        case "POST":
            curl_setopt($curl, CURLOPT_POST, 1);
            if ($data)
                curl_setopt($curl, CURLOPT_POSTFIELDS, $data);
            break;
        case "PUT":
            curl_setopt($curl, CURLOPT_PUT, 1);
            break;
        default:
            if ($data)
                $url = sprintf("%s?%s", $url, http_build_query($data));
    }


    curl_setopt($curl, CURLOPT_URL, $url);
    curl_setopt($curl, CURLOPT_FOLLOWLOCATION, true);
    curl_setopt($curl, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($curl, CURLOPT_HTTPHEADER, $headers); 
    $result = curl_exec($curl);

    curl_close($curl);

    return $result;
}

save_order($body, $url);
save_order_items($body, $url);
header('Content-Type: application/json; charset=utf-8');
echo json_encode(['success' => true]);
