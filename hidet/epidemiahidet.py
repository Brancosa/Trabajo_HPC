import hidet
import torch

# take resnet18 as an example
x = torch.randn(1, 3, 224, 224, dtype=torch.float16).cuda()
model = torch.hub.load('pytorch/vision:v0.9.0', 'resnet18', pretrained=True, verbose=False)
model = model.cuda().eval().to(torch.float16)

# optimize the model with 'hidet' backend
model_opt = torch.compile(model, backend='hidet', mode='max-autotune')

# run the optimized model
y1 = model_opt(x)
y2 = model(x)

# check the correctness
torch.testing.assert_close(actual=y1, expected=y2, rtol=2e-2, atol=2e-2)


# benchmark the performance
for name, model in [('eager', model), ('hidet', model_opt)]:
    start_event = torch.cuda.Event(enable_timing=True)
    end_event = torch.cuda.Event(enable_timing=True)
    torch.cuda.synchronize()
    start_event.record()
    for _ in range(100):
        y = model(x)
    end_event.record()
    torch.cuda.synchronize()
    print('{:>10}: {:.3f} ms'.format(name, start_event.elapsed_time(end_event) / 100.0))