<template>
  <button class="voice-call-button" @click="startVoiceCall">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z" 
            fill="currentColor"/>
      <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z" 
            fill="currentColor"/>
    </svg>
    <span>{{ buttonText }}</span>
  </button>
</template>

<script>
import { useRouter } from 'vue-router';

export default {
  name: 'VoiceCallButton',
  props: {
    buttonText: {
      type: String,
      default: '开始语音通话'
    }
  },
  setup() {
    const router = useRouter();

    const startVoiceCall = () => {
      router.push('/voice-call');
    };

    return {
      startVoiceCall
    };
  }
};
</script>

<style scoped>
.voice-call-button {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 2rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  border-radius: 12px;
  color: white;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.voice-call-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
}

.voice-call-button:active {
  transform: translateY(0);
}

.voice-call-button svg {
  flex-shrink: 0;
}
</style>

