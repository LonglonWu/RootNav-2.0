import pydensecrf.densecrf as dcrf
import numpy as np

class CRF():
    @staticmethod
    def ApplyCRF(model_softmax, image):
        image = np.ascontiguousarray(image)
        unary = -np.log(model_softmax)
        unary = unary.transpose(2, 1, 0)
        w, h, c = unary.shape
        unary = unary.transpose(2, 0, 1)
        unary = unary.reshape(6, -1)
        unary = np.ascontiguousarray(unary)
        
        d = dcrf.DenseCRF2D(w, h, 6)
        d.setUnaryEnergy(unary)
        d.addPairwiseBilateral(sxy=5, srgb=3, rgbim=image, compat=1)
        q = d.inference(50)
        mask = np.argmax(q, axis=0).reshape(w, h).transpose(1, 0)
        return mask

    @staticmethod
    def decode_channel(mask, index):
        channel_out = np.zeros(mask.shape, dtype=np.uint8)
        if isinstance(index, list):
            for i in index:
                channel_out[mask == i] = 255
        else:
            channel_out[mask == index] = 255

        return channel_out