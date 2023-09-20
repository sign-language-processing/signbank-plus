## Fairseq

### Train Systems
```bash
sbatch train.sh \
  /home/amoryo/sign-language/signbank-annotation/signbank-plus/data/parallel/original \
  /shares/volk.cl.uzh/amoryo/checkpoints/fairseq/original
  
sbatch train.sh \
  /home/amoryo/sign-language/signbank-annotation/signbank-plus/data/parallel/cleaned \
  /shares/volk.cl.uzh/amoryo/checkpoints/fairseq/cleaned
   
sbatch train.sh \
  /home/amoryo/sign-language/signbank-annotation/signbank-plus/data/parallel/expanded \
  /shares/volk.cl.uzh/amoryo/checkpoints/fairseq/expanded 
```

### Eval Systems

Wait for all systems to finish training
```bash
sbatch eval.sh \
  /home/amoryo/sign-language/signbank-annotation/signbank-plus/data/parallel/test \
  /shares/volk.cl.uzh/amoryo/checkpoints/fairseq/original
  
sbatch eval.sh \
  /home/amoryo/sign-language/signbank-annotation/signbank-plus/data/parallel/test \
  /shares/volk.cl.uzh/amoryo/checkpoints/fairseq/cleaned
  
sbatch eval.sh \
  /home/amoryo/sign-language/signbank-annotation/signbank-plus/data/parallel/test \
  /shares/volk.cl.uzh/amoryo/checkpoints/fairseq/expanded
```



