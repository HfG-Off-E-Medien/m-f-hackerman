import cv2
import numpy as np
import os
from subprocess import call

def before_stitched(img, overlap):
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
    fade_inverse = 1.0 / apply_fades(np.ones(img.shape), overlap=overlap)
    states = []
    x_vals, y_vals = compute_vals(len_x, overlap, ps), compute_vals(len_y, overlap, ps)

    i=0
    for x in range(len(x_vals) - 1):
        x_start = x_vals[x]
        x_end   = x_vals[x+1] + overlap
        x_start_patch = np.clip(x_start, None, len_x - ps)
        x_end_patch   = np.clip(x_end, ps, None)
        for y in range(len(y_vals) - 1):
            y_start = y_vals[y]
            y_end   = y_vals[y+1] + overlap
            y_start_patch = np.clip(y_start, None, len_y - ps)
            y_end_patch   = np.clip(y_end, ps, None)
              
            # obtain patch and pass thru network
            patch = img[x_start_patch : x_end_patch, y_start_patch : y_end_patch]
            cv2.imwrite('./CUT/datasets/test/testB/'+str(i)+'.jpg', patch)
            cv2.imwrite('./CUT/datasets/test/testA/'+str(i)+'.jpg', patch)
            cv2.imwrite('./CUT/datasets/test/trainA/'+str(i)+'.jpg', patch)
            cv2.imwrite('./CUT/datasets/test/trainB/'+str(i)+'.jpg', patch)
            i += 1
    return i

def render_stitched(img, overlap, out_path):
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
    fade_inverse = 1.0 / apply_fades(np.ones(img.shape), overlap=overlap)
    states = []
    x_vals, y_vals = compute_vals(len_x, overlap, ps), compute_vals(len_y, overlap, ps)

    i=0
    for x in range(len(x_vals) - 1):
        x_start = x_vals[x]
        x_end   = x_vals[x+1] + overlap
        x_start_patch = np.clip(x_start, None, len_x - ps)
        x_end_patch   = np.clip(x_end, ps, None)
        for y in range(len(y_vals) - 1):
            y_start = y_vals[y]
            y_end   = y_vals[y+1] + overlap
            y_start_patch = np.clip(y_start, None, len_y - ps)
            y_end_patch   = np.clip(y_end, ps, None)
              
            # obtain patch and pass thru network
            patch = cv2.imread('./results/test/test_latest/images/fake_B/'+str(i)+'.png')
            patch = np.float32(patch) / 127.5 - 1
            tmp[x_start_patch : x_end_patch, y_start_patch : y_end_patch] = np.copy(patch)
            patch = tmp[x_start : x_end, y_start : y_end]
            patch = apply_fades(patch, overlap)
            out[x_start : x_end, y_start : y_end] += patch
            state = np.uint8(np.clip((out*fade_inverse+1)*127.5, 0, 255))
            #states.append(state)
            cv2.imwrite(out_path, state)
            i += 1

class Pipeline():
    def __init__(self):
        self.overlap = 128

    def run(self, img_path, out_path):
        self.clean_dirs()
        print('Calling the pipeline...')
        img = cv2.imread(img_path)
        print('Chopping image...')
        num_patches = before_stitched(img, self.overlap)
        print('Applying AI filter to image chops...')
        call(["python", "/home/ki-lab-02/Desktop/Studentische-Projekte/Moritz/SERVER/CUT/test.py", "--dataroot", "/home/ki-lab-02/Desktop/Studentische-Projekte/Moritz/SERVER/CUT/datasets/test", "--name", "test", "--CUT_mode", "CUT", "--phase", "test"])
        #exec("python ./CUT/test.py --dataroot ./datasets/test --name test --CUT_mode CUT --phase test")
        print('Stitching chops back together...')
        render_stitched(img, self.overlap, out_path)
        print('Done.')

    def warump(self):
        cv2.imwrite("warmup_in.jpg", np.uint8(255*np.random.uniform(0,1, size=(1000,1000,3))))
        self.run("warmup_in.jpg", "warmup_out.jpg")
    
    def clean_dirs(self):
        def clean(dir):
            for file in os.listdir(dir):
                os.remove(dir+file)
        
        clean('./CUT/datasets/test/testB/')
        clean('./CUT/datasets/test/testA/')
        clean('./CUT/datasets/test/trainA/')
        clean('./CUT/datasets/test/trainB/')

            