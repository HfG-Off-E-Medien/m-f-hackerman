import numpy as np
import cv2

class Patcher():
    def __init__(self,
                 output_dir,
                 overlap = 128):

        self.output_dir = output_dir
        self.overlap = overlap

    def split_image_into_patches(self, output_dir, img):
        def compute_vals(sidelen, overlap, ps):
            adjusted_ps = ps - overlap
            n_add_patches = (sidelen - ps) // adjusted_ps
            patches_span = ps + n_add_patches * adjusted_ps
            shift = (sidelen - patches_span) // 2
            vals = list(range(shift, shift + patches_span, adjusted_ps))
            if vals[0] != 0:
                vals = [0,] + vals
            if vals[-1] != sidelen:
                vals = vals + [sidelen,]
            return vals

        def apply_fades(x, overlap):
            # left/right
            left = np.linspace(0, 1, overlap+2)[1:-1]
            left = np.expand_dims(left, axis=0)
            left = np.repeat(left, repeats=x.shape[0], axis=0)
            x[:,:overlap] *= np.expand_dims(left, -1)
            right = np.flip(left, axis=1)
            x[:,-overlap:] *= np.expand_dims(right, -1)
            # top/bot
            top = np.linspace(0, 1, overlap+2)[1:-1]
            top = np.expand_dims(top, 0)
            top = np.transpose(top, (1,0))
            top = np.repeat(top, repeats=x.shape[1], axis=1)
            x[:overlap,:] *= np.expand_dims(top, -1)
            bot = np.flip(top, axis=0)
            x[-overlap:,:] *= np.expand_dims(bot, -1)
            return x

        ps = 256
        len_x, len_y = img.shape[0], img.shape[1]
        img_uint8 = img+0
        out = np.zeros(img.shape)
        tmp = np.copy(out)
        fade_inverse = 1.0 / apply_fades(np.ones(img.shape), overlap=self.overlap)
        states = []
        x_vals, y_vals = compute_vals(len_x, self.overlap, ps), compute_vals(len_y, self.overlap, ps)

        i=0
        for x in range(len(x_vals) - 1):
            x_start = x_vals[x]
            x_end   = x_vals[x+1] + self.overlap
            x_start_patch = np.clip(x_start, None, len_x - ps)
            x_end_patch   = np.clip(x_end, ps, None)
            for y in range(len(y_vals) - 1):
                y_start = y_vals[y]
                y_end   = y_vals[y+1] + self.overlap
                y_start_patch = np.clip(y_start, None, len_y - ps)
                y_end_patch   = np.clip(y_end, ps, None)

                # obtain patch and save
                patch = img[x_start_patch : x_end_patch, y_start_patch : y_end_patch]
                cv2.imwrite(output_dir+str(i)+'.jpg', patch)
                i += 1
        #return i