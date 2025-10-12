from TeamControl.network.ssl_sockets import Vision

def test_vision_initialization():
    vision = Vision()
    print(vision.addr)
    assert vision is not None
    data = vision.listen()
    # assert data is not None
    print(data)
    
test_vision_initialization()