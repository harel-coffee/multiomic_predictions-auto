# MLP MODELS

| Views  | ACC | Prec | Rec  | F1   |
| -------|:---:| :---:| :---:| :---:|
|__All__ |95.43 |95.638 |95.43 |95.412 |
|__CNV__ |25.087 |28.224 |25.087 |23.642 |
|__EXON__ |92.566 |93.196 |92.566 |92.693 |
|__METHYL__ |93.417 |93.826 |93.417 |93.53 |
|__MiRNA__ |95.249 |95.393 |95.249 |95.246 |
|__Protein__ |95.114 |95.831 |95.114 |95.333 |
|__RNA_ISO__ |94.762 |95.006 |94.762 |94.825 |
|__RNA__ |94.898 |95.559 |94.898 |95.061 |

# TRANSFORMERS
Default dropout =0.1

Default combinaison is the same caracteristic for encoder and decoder (unless precise)


| HyperParametersComb(d_model/d_ff/n_heads/n_layers)  | ACC | Prec | Rec  | F1   |
| -------|:---:| :---:| :---:| :---:|
|__256_1024_4_2__ |90.755 |92.159 |90.755 |91.065 |
|__256_1024_8_4/256_1024_4_2__ |89.373 |91.387 |89.373 |89.611 |
|__256_1024_8_4__ |87.779 |89.384 |87.779 |87.983 |
|__256_1024_16_8__ |89.692 |90.521 |89.692 |89.79 |
|__64_256_2_6__ |88.31 |90.676 |88.31 |88.603 |
|__64_256_8_12__ |86.929 |88.993 |86.929 |87.126 |
|__512_2048_16_4_droupout=0.2__ |85.016 |87.86 |85.016 |85.064 |
|__512_2048_4_8__ |90.223 |90.954 |90.223 |90.306 |


Views ALL: regroupe tous les patients qui ont plus d'une vue de disponible (nb_view >=2 )