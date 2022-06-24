
import base64

def isBase64(sb):
        try:
                if isinstance(sb, str):
                        # If there's any unicode here, an exception will be thrown and the function will return false
                        sb_bytes = bytes(sb, 'ascii')
                elif isinstance(sb, bytes):
                        sb_bytes = sb
                else:
                        raise ValueError("Argument must be string or bytes")
                return base64.b64encode(base64.b64decode(sb_bytes)) == sb_bytes
        except Exception:
                return False


def encode_base64(string: str):
 string = string.encode("ascii")
   
 base64_bytes = base64.b64encode(string)
 return base64_bytes.decode("ascii")


def decode_base64(string:str):
    return base64.b64decode(string)
