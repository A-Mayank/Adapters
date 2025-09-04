# Adapters
ADPTER TRAINING GUIDE

===========================================================================

THIS FILE WILL HELP TO UNDERSTAND THE PROCESS OF TRAINING AND EVALUATING AN ADAPTER.

PREREQUISITES
1. How an adapter setup works.
     reference - [https://arxiv.org/abs/2005.00052](MAD-X Paper)

2. NER Datset preprocessing.
    reference - [https://www.youtube.com/watch?v=dzyDHMycx_c](Youtube)

3. Adapters - [https://docs.adapterhub.ml/quickstart.html] (Adapter Introduction)

--------------------------------------------------------------------------------
DATASET PREPROCESSING

Preprcoessing is divided into 3 parts .
1. Langauge Adapter Preprocessing
2. Task Adapter Preprocessing
3. Evaluation Dataset preprocessing


Set the labels for NER Tags:
  {"O": 0, "B-per": 1, "I-per": 2, "B-org": 3, "I-org": 4, "B-loc": 5, "I-loc": 6}

  This is default TAG List for BIO Tagging Format. 
   
--------------------------------------------------------------------------------

Language Adapter Training:
 
1. We start with training the language adapter, these adapters will be trained on 
   unlabeled data.

2. In `language.ipynb` give the directory of the unlabled dataset and RUN,
   this will automatically save the langauge adapter in your folder.

3. You can change the adapter name and ouput directory accordingly.

NOTE: SAME PIPELINE CAN BE USED FOR TRAINING TARGET LANGUAGE ADAPTER. 

--------------------------------------------------------------------------------

Task Adapter Training:


1. RUN `task.ipynb` for TASK ADAPTER Training.

2. This adapter would be trained on labeled dataset, for this project NER Dataset have
   been used.

3. Set the path for NER Dataset, preprocess pipeline will convert the dataset into 
   Huggingface Dict. i.e. the format for tokenizing the text. After Ist preprocess your 
   output should be:

    DatasetDict({
    train: Dataset({
        features: ['LABEL-1', 'LABEL-2']
    })
  })

 NOTE: You can change name of the labels, the NER dataset used was having ['token','ner_tags'] as label.

4. This preprocessing will tokenize and map the text to their corresponding input_ids.
   Your ouput should be:

   DatasetDict({
    train: Dataset({
        features: ['LABEL-1', 'LABEL-2', 'input_ids', 'attention_mask', 'labels'],
     })
   }) 

5. We shall remove the LABELS from the Dataset for training purpose.

6. Import a pretrained adapter model for training. Add your adapter ['model.add_adapter("Your_Task_Adapter")'].
   this adapter would then be stacked with Language Adpater. 

   NOTE:The langauge adapter should be same as the langauage being used for training Task Adapter.

7. Set your parameters for training.

8. Save your Task adapter for further evalauation.
 

--------------------------------------------------------------------------------

Evaluation: 

1. We would evaluate on Target Adapter language. Evaluation would be done for labeled 
   dataset of the langauge.

2. So we would preprcoess the data same way we did for Task Adapter Dataset.
   Repat the process till removing the LABELS.

3. Then we will call the TASK ADAPTER and replace the Language adapter with 
   Target adapter. 

4. Then would evaluate for test split of the dataset.

--------------------------------------------------------------------------------

SINCE WE USED NER DATASET, WE SAW A HUGE CLASS IMBALANCE IN TAGGING, SO DURING EVALUATION
WE WOULD IGNORE THE DOMINATED TAG FOR BETTER RESULTS.

YOU CAN TRY ANOTHER APPROACH TO EVALAUTE 

--------------------------------------------------------------------------------


INSTALL THE REQUIRED PACKAGES FROM 'requirements.txt'
