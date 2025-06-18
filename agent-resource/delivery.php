<?php
$uri =  $_SERVER['REQUEST_URI'];
$method =  $_SERVER['REQUEST_METHOD'];

function get_delivery(){
	return [
		'data' => [
			'NORMAL' => [
				'delivery_type' => 'NORMAL',
				'description' => 'Giao hàng bình thường (2-3 ngày)',
				'shipping_fee' => 0,
				'is_default' => 'Yes',
				'currency' => 'VND'
			],
			'EXPRESS_IN_DAY' => [
				'delivery_type' => 'EXPRESS_IN_DAY',
				'description'  => 'Giao hàng nhanh trong ngày.',
				'shipping_fee' => rand(10, 20) * 1000,
				// 'shipping_fee' => 18000,
				'is_default' => 'No',
				'currency' => 'VND'
			],
			'EXPRESS_2_HOURS' => [
				'delivery_type' => 'EXPRESS_2_HOURS',
				'description'  => 'Giao hàng nhanh trong 2 giờ.',
				'shipping_fee' => rand(25, 35) * 1000,
				// 'shipping_fee' => 25000,
				'is_default' => 'No',
				'currency' => 'VND'
			]
		]
	];
    
}

header('Content-Type: application/json; charset=utf-8');
echo json_encode(get_delivery());