// src/components/calls/VideoCall.vue
<template>
  <div class="relative w-full h-full bg-gray-900">
    <!-- Remote Video (Full Screen) -->
    <video
      ref="remoteVideo"
      class="w-full h-full object-cover"
      autoplay
      playsinline
    ></video>

    <!-- Local Video (Small Overlay) -->
    <video
      ref="localVideo"
      class="absolute bottom-4 right-4 w-48 h-36 object-cover rounded-lg border-2 border-white"
      autoplay
      playsinline
      muted
    ></video>

    <!-- Call Controls -->
    <div class="absolute bottom-4 left-1/2 transform -translate-x-1/2 flex space-x-4">
      <button
        @click="toggleMute"
        class="p-4 rounded-full"
        :class="isMuted ? 'bg-red-600' : 'bg-gray-700'"
      >
        <span class="text-white">
          {{ isMuted ? 'Unmute' : 'Mute' }}
        </span>
      </button>

      <button
        @click="toggleVideo"
        class="p-4 rounded-full"
        :class="isVideoOff ? 'bg-red-600' : 'bg-gray-700'"
      >
        <span class="text-white">
          {{ isVideoOff ? 'Start Video' : 'Stop Video' }}
        </span>
      </button>

      <button
        @click="endCall"
        class="p-4 bg-red-600 rounded-full"
      >
        <span class="text-white">End Call</span>
      </button>
    </div>

    <!-- Incoming Call Modal -->
    <div 
      v-if="incomingCall"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center"
    >
      <div class="bg-white p-6 rounded-lg text-center">
        <h3 class="text-lg font-medium mb-4">
          Incoming call from {{ incomingCall.caller.name }}
        </h3>
        <div class="flex justify-center space-x-4">
          <button
            @click="acceptCall"
            class="px-4 py-2 bg-green-600 text-white rounded-md"
          >
            Accept
          </button>
          <button
            @click="rejectCall"
            class="px-4 py-2 bg-red-600 text-white rounded-md"
          >
            Reject
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue'
import { useStore } from 'vuex'
import io from 'socket.io-client'

export default {
  name: 'VideoCall',
  props: {
    roomId: {
      type: String,
      required: true
    },
    isInitiator: {
      type: Boolean,
      default: false
    }
  },
  setup(props) {
    const store = useStore()
    const socket = ref(null)
    const peerConnection = ref(null)
    const localStream = ref(null)
    const remoteStream = ref(null)
    const localVideo = ref(null)
    const remoteVideo = ref(null)
    const isMuted = ref(false)
    const isVideoOff = ref(false)
    const incomingCall = ref(null)

    // WebRTC configuration
    const configuration = {
      iceServers: [
        { urls: 'stun:stun.l.google.com:19302' }
      ]
    }

    const initializeWebRTC = async () => {
      try {
        // Get local media stream
        localStream.value = await navigator.mediaDevices.getUserMedia({
          video: true,
          audio: true
        })
        
        // Display local video
        if (localVideo.value) {
          localVideo.value.srcObject = localStream.value
        }

        // Create peer connection
        peerConnection.value = new RTCPeerConnection(configuration)

        // Add local stream to peer connection
        localStream.value.getTracks().forEach(track => {
          peerConnection.value.addTrack(track, localStream.value)
        })

        // Handle incoming tracks
        peerConnection.value.ontrack = (event) => {
          remoteStream.value = event.streams[0]
          if (remoteVideo.value) {
            remoteVideo.value.srcObject = remoteStream.value
          }
        }

        // Connect to signaling server
        socket.value = io('http://localhost:5000')

        // Join room
        socket.value.emit('join-room', props.roomId)

        // Handle signaling
        socket.value.on('offer', async (offer) => {
          if (!props.isInitiator) {
            await peerConnection.value.setRemoteDescription(offer)
            const answer = await peerConnection.value.createAnswer()
            await peerConnection.value.setLocalDescription(answer)
            socket.value.emit('answer', answer, props.roomId)
          }
        })

        socket.value.on('answer', async (answer) => {
          if (props.isInitiator) {
            await peerConnection.value.setRemoteDescription(answer)
          }
        })

        socket.value.on('ice-candidate', async (candidate) => {
          try {
            await peerConnection.value.addIceCandidate(candidate)
          } catch (error) {
            console.error('Error adding ICE candidate:', error)
          }
        })

        // Handle ICE candidates
        peerConnection.value.onicecandidate = (event) => {
          if (event.candidate) {
            socket.value.emit('ice-candidate', event.candidate, props.roomId)
          }
        }

        // If initiator, create and send offer
        if (props.isInitiator) {
          const offer = await peerConnection.value.createOffer()
          await peerConnection.value.setLocalDescription(offer)
          socket.value.emit('offer', offer, props.roomId)
        }

      } catch (error) {
        console.error('Error initializing WebRTC:', error)
      }
    }

    const toggleMute = () => {
      if (localStream.value) {
        localStream.value.getAudioTracks().forEach(track => {
          track.enabled = !track.enabled
          isMuted.value = !track.enabled
        })
      }
    }

    const toggleVideo = () => {
      if (localStream.value) {
        localStream.value.getVideoTracks().forEach(track => {
          track.enabled = !track.enabled
          isVideoOff.value = !track.enabled
        })
      }
    }

    const endCall = async () => {
      try {
        // Stop all tracks
        if (localStream.value) {
          localStream.value.getTracks().forEach(track => track.stop())
        }
        
        // Close peer connection
        if (peerConnection.value) {
          peerConnection.value.close()
        }
        
        // Disconnect socket
        if (socket.value) {
          socket.value.disconnect()
        }

        // Update call status in backend
        await store.dispatch('calls/endCall', props.roomId)

        // Navigate back
        window.history.back()
      } catch (error) {
        console.error('Error ending call:', error)
      }
    }

    onMounted(() => {
      initializeWebRTC()
    })

    onUnmounted(() => {
      endCall()
    })

    return {
      localVideo,
      remoteVideo,
      isMuted,
      isVideoOff,
      incomingCall,
      toggleMute,
      toggleVideo,
      endCall
    }
  }
}
</script>

