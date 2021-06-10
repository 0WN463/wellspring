import inspect
import matplotlib.pyplot as plt

def show_implementation(cls, section=None):
    SECTION_DELIMITER = "Section "
    found_section = False
    it = inspect.getsourcelines(cls)[0]
    print(it[0])
    for line in it[1:]:
        if section is not None and section not in line and not found_section:
            continue
        found_section = True
        
        if SECTION_DELIMITER in line and section is not None and section not in line:
            break
        print(line, end='')
        
def show_images(img_label_tuples, grey=True, autoscale=False):
    n = len(img_label_tuples)
    f = plt.figure(figsize=(20,10))
    
    axes = [f.add_subplot(100 + 10 * n + i) for i in range(1, n+1)]
    
    vmax = 1 if all([image.max() <= 1 for image, _ in img_label_tuples]) else 255
    

    for ax, (image, label) in zip(axes, img_label_tuples):
        ax.title.set_text(label)
        if autoscale:
            vmax = image.max()
        if grey:
            ax.imshow(image, cmap='gray', vmin=0, vmax=vmax)
        else:
            ax.imshow(image)
            
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)

