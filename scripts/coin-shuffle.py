import glob
import numpy as np

if __name__ =="__main__":
    print("Shuffle count!")

    coin_prefix_set = ["coin10","coin20","coin100"]
    coin_sufix_set = ["2","0","1"]
    
    for px,coin_prefix in enumerate(coin_prefix_set):
    
        image_reduced_path="/home/mhuertas/Work/RoboND/Project2/reduced/"+coin_prefix+"/"
        image_names = glob.glob(image_reduced_path+"*.jpg")
        
        image_names_px = np.random.randint(1,len(image_names)-1,10)
        for image_px in  image_names_px:
            print(coin_prefix+"/output_"+ str(image_px).zfill(4) +"_"+coin_sufix_set[px]+".jpg")