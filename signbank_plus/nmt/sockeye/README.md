## Sockeye

### Train Systems
```bash
sbatch train.sh \
  /home/amoryo/sign-language/signbank-annotation/signbank-plus/data/parallel/original \
  /shares/volk.cl.uzh/amoryo/checkpoints/sockeye/original
  
sbatch train.sh \
  /home/amoryo/sign-language/signbank-annotation/signbank-plus/data/parallel/cleaned \
  /shares/volk.cl.uzh/amoryo/checkpoints/sockeye/cleaned
   
sbatch train.sh \
  /home/amoryo/sign-language/signbank-annotation/signbank-plus/data/parallel/expanded \
  /shares/volk.cl.uzh/amoryo/checkpoints/sockeye/expanded 
     
# Fine tune expanded on cleaned 
sbatch train.sh \
  /home/amoryo/sign-language/signbank-annotation/signbank-plus/data/parallel/cleaned \
  /shares/volk.cl.uzh/amoryo/checkpoints/sockeye/expanded-cleaned \
  /shares/volk.cl.uzh/amoryo/checkpoints/sockeye/expanded 
```

### Eval Systems

Wait for all systems to finish training
```bash
sbatch eval.sh \
  /home/amoryo/sign-language/signbank-annotation/signbank-plus/data/parallel/test \
  /shares/volk.cl.uzh/amoryo/checkpoints/sockeye/original
  
sbatch eval.sh \
  /home/amoryo/sign-language/signbank-annotation/signbank-plus/data/parallel/test \
  /shares/volk.cl.uzh/amoryo/checkpoints/sockeye/cleaned

sbatch eval.sh \
  /home/amoryo/sign-language/signbank-annotation/signbank-plus/data/parallel/test \
  /shares/volk.cl.uzh/amoryo/checkpoints/sockeye/expanded
  
sbatch eval.sh \
  /home/amoryo/sign-language/signbank-annotation/signbank-plus/data/parallel/test \
  /shares/volk.cl.uzh/amoryo/checkpoints/sockeye/expanded-cleaned
```

