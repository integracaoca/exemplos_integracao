<?php

// Obter o método HTTP e a rota solicitada
$method = $_SERVER['REQUEST_METHOD'];
$uri = $_SERVER['REQUEST_URI'];

// printa o method e uri no console 
error_log("Method: $method, URI: $uri");

// Rota: /notification (POST)
if ($method === 'POST') {
    header('Content-Type: application/json');
    header('Content-Length: 68');
    echo json_encode([
        'auth' => 'true',
        'code' => '200',
        'message' => 'Notification received successfully'
    ]);
    http_response_code(200);
    exit;
}

// 
if ($method === 'GET') {
    // content lengthv é essencial para o disposistivo.
    header('Content-Length: 2');
    header('Content-Type: text/html; charset=UTF-8');
    http_response_code(200);
    echo "OK";
    exit;
}

// Resposta padrão para rotas desconhecidas
http_response_code(404);
echo json_encode(['error' => 'Route not found'])
?>