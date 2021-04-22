# multiomic_predictions

## Important parameters to remember while building the configs file

1. __dataset_views_to_consider__ must be precise. Values must be in
    1. __all__, load all the 8 views (cnv, methyl27, methyl450,exon, mirna, rna, rna_iso, protein),
    2. __cnv__, load just cnv views,
    3. __methyl__, load just methyl27 and methyl450 views
    4. __exon__, load just exon views
    5. __mirna__, load just mirna views
    6. __rna__, load just rna views
    7. __rna_iso__, load just rna_iso views
    8. __protein__, load just protein views

2. __type_of_model__ must be precise. Right now it is just:
    1. __transformer__ (return dataset shape[views, 2000] and
    2. __mlp__ return dataset shpae[1, 2000 or 16000].

## Command form to run the code

__Transformer__

    run_multiomic_models dispatch --server 'graham' --config-file '/home/maoss2/PycharmProjects/multiomic_predictions/expts/configs/transformer_all_config_7.json' --exp-name 'all_multiomic_transformer_7' --cpus '4' --memory '4G' --duration '05:00:00' --output-path '/home/maoss2/scratch/expts_results'

    run_multiomic_models dispatch --server 'graham' --config-file '/home/maoss2/PycharmProjects/multiomic_predictions/expts/configs/transformer_all_config_6.json' --exp-name 'all_multiomic_transformer_6' --cpus '4' --memory '4G' --duration '05:00:00' --output-path '/home/maoss2/scratch/expts_results'

    run_multiomic_models dispatch --server 'graham' --config-file '/home/maoss2/PycharmProjects/multiomic_predictions/expts/configs/transformer_all_config_5.json' --exp-name 'all_multiomic_transformer_5' --cpus '4' --memory '4G' --duration '05:00:00' --output-path '/home/maoss2/scratch/expts_results'

    run_multiomic_models dispatch --server 'graham' --config-file '/home/maoss2/PycharmProjects/multiomic_predictions/expts/configs/transformer_all_config_5.json' --exp-name 'all_multiomic_transformer_5' --cpus '4' --memory '4G' --duration '05:00:00' --output-path '/home/maoss2/scratch/expts_results'

    run_multiomic_models dispatch --server 'graham' --config-file '/home/maoss2/PycharmProjects/multiomic_predictions/expts/configs/transformer_all_config_4.json' --exp-name 'all_multiomic_transformer_4' --cpus '4' --memory '4G' --duration '05:00:00' --output-path '/home/maoss2/scratch/expts_results'

    run_multiomic_models dispatch --server 'graham' --config-file '/home/maoss2/PycharmProjects/multiomic_predictions/expts/configs/transformer_all_config_3.json' --exp-name 'all_multiomic_transformer_3' --cpus '4' --memory '4G' --duration '05:00:00' --output-path '/home/maoss2/scratch/expts_results'

    run_multiomic_models dispatch --server 'graham' --config-file '/home/maoss2/PycharmProjects/multiomic_predictions/expts/configs/transformer_all_config_2.json' --exp-name 'all_multiomic_transformer_2' --cpus '4' --memory '4G' --duration '05:00:00' --output-path '/home/maoss2/scratch/expts_results'

    run_multiomic_models dispatch --server 'graham' --config-file '/home/maoss2/PycharmProjects/multiomic_predictions/expts/configs/transformer_all_config_1.json' --exp-name 'all_multiomic_transformer_1' --cpus '4' --memory '4G' --duration '05:00:00' --output-path '/home/maoss2/scratch/expts_results'

    run_multiomic_models dispatch --server 'graham' --config-file '/home/maoss2/PycharmProjects/multiomic_predictions/expts/configs/transformer_all_config_0.json' --exp-name 'all_multiomic_transformer_0' --cpus '4' --memory '4G' --duration '05:00:00' --output-path '/home/maoss2/scratch/expts_results'
    
__MLP__

    run_mlp_models dispatch --server 'graham' --config-file '/home/maoss2/PycharmProjects/multiomic_predictions/expts/configs/mlp_all_config.json' --exp-name 'all_multiomic_mlp' --cpus '1' --memory '4G' --duration '01:00:00' --output-path '/home/maoss2/scratch/expts_results'

    run_mlp_models dispatch --server 'graham' --config-file '/home/maoss2/PycharmProjects/multiomic_predictions/expts/configs/mlp_cnv_config.json' --exp-name 'cnv_multiomic_mlp' --cpus '1' --memory '4G' --duration '00:30:00' --output-path '/home/maoss2/scratch/expts_results'

    run_mlp_models dispatch --server 'graham' --config-file '/home/maoss2/PycharmProjects/multiomic_predictions/expts/configs/mlp_exon_config.json' --exp-name 'exon_multiomic_mlp' --cpus '1' --memory '4G' --duration '00:30:00'  --output-path '/home/maoss2/scratch/expts_results'

    run_mlp_models dispatch --server 'graham' --config-file '/home/maoss2/PycharmProjects/multiomic_predictions/expts/configs/mlp_methyl_config.json' --exp-name 'methyl_multiomic_mlp' --cpus '1' --memory '4G' --duration '00:30:00' --output-path '/home/maoss2/scratch/expts_results'

    run_mlp_models dispatch --server 'graham' --config-file '/home/maoss2/PycharmProjects/multiomic_predictions/expts/configs/mlp_mirna_config.json' --exp-name 'mirna_multiomic_mlp' --cpus '1' --memory '4G' --duration '00:30:00' --output-path '/home/maoss2/scratch/expts_results'

    run_mlp_models dispatch --server 'graham' --config-file '/home/maoss2/PycharmProjects/multiomic_predictions/expts/configs/mlp_protein_config.json' --exp-name 'protein_multiomic_mlp' --cpus '1' --memory '4G' --duration '00:30:00' --output-path '/home/maoss2/scratch/expts_results'

    run_mlp_models dispatch --server 'graham' --config-file '/home/maoss2/PycharmProjects/multiomic_predictions/expts/configs/mlp_rna_config.json' --exp-name 'rna_multiomic_mlp' --cpus '1' --memory '4G' --duration '00:30:00' --output-path '/home/maoss2/scratch/expts_results'

    run_mlp_models dispatch --server 'graham' --config-file '/home/maoss2/PycharmProjects/multiomic_predictions/expts/configs/mlp_rna_iso_config.json' --exp-name 'rna_iso_multiomic_mlp' --cpus '1' --memory '4G' --duration '00:30:00' --output-path '/home/maoss2/scratch/expts_results'

    run_mlp_models dispatch --server 'local' --config-file 'expts/configs/mlp_all_config.json' --exp-name 'mlp_debuging' --cpus 2