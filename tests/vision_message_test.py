"""
Run this to check if you can receive data from SSL VISION Or GRSIM at port 10006
"""

from TeamControl.network.ssl_sockets import Vision

def test_vision_initialization():
    vision = Vision()
    print(vision.addr)
    assert vision is not None
    data = vision.listen()
    # assert data is not None
    print(data)
    
test_vision_initialization()