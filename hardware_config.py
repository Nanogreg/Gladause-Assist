class HardwareConfig:
    """ System configuration for text generation """
    
    default_cpu_cores = 8       # Your number of physical CPU cores
    default_gpu_offload = 0     # GPU offload : 0 = auto (ollama). 99 = max
    default_system_ram = 16     # System ram for CPU generation, VRAM for GPU generation
    
    def __init__ (self, cpu_cores: int = default_cpu_cores, gpu_offload: int = default_gpu_offload, system_ram: int = default_system_ram):
        self.cpu_cores = cpu_cores
        self.gpu_offload = gpu_offload
        self.system_ram = system_ram
        self.num_ctx = self.set_num_ctx()
        
    def set_num_ctx(self):
        if self.system_ram <= 8:
            return 1024
        elif self.system_ram <= 12:
            return 2048
        elif self.system_ram <= 16:
            return 4096
        else:
            return 8192