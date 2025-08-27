/**
 * Medical Drug Information Chatbot - Frontend JavaScript
 */

class MedicalChatbot {
    constructor() {
        this.isProcessing = false;
        this.messageCount = 0;
        this.init();
    }

    init() {
        this.bindEvents();
        this.setupFileUpload();
        this.focusInput();
        this.checkHealth();
    }

    bindEvents() {
        // Chat form submission
        $('#chatForm').on('submit', (e) => {
            e.preventDefault();
            this.sendMessage();
        });

        // Quick question buttons
        $('.quick-question').on('click', (e) => {
            const question = $(e.target).data('question');
            $('#messageInput').val(question);
            this.sendMessage();
        });

        // Clear session button
        $('#clearSession').on('click', () => {
            this.clearSession();
        });

        // Enter key handling
        $('#messageInput').on('keypress', (e) => {
            if (e.which === 13 && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // Auto-resize input
        $('#messageInput').on('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
    }

    setupFileUpload() {
        const uploadInput = $('#pdfUpload');
        
        uploadInput.on('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                this.uploadFile(file);
            }
        });

        // Drag and drop functionality
        const chatMessages = $('#chatMessages');
        
        chatMessages.on('dragover', (e) => {
            e.preventDefault();
            chatMessages.addClass('dragover');
        });

        chatMessages.on('dragleave', (e) => {
            e.preventDefault();
            chatMessages.removeClass('dragover');
        });

        chatMessages.on('drop', (e) => {
            e.preventDefault();
            chatMessages.removeClass('dragover');
            
            const files = e.originalEvent.dataTransfer.files;
            if (files.length > 0) {
                const file = files[0];
                if (file.type === 'application/pdf') {
                    this.uploadFile(file);
                } else {
                    this.showError('Please upload only PDF files.');
                }
            }
        });
    }

    async sendMessage() {
        const input = $('#messageInput');
        const message = input.val().trim();

        if (!message || this.isProcessing) {
            return;
        }

        // Clear input and disable form
        input.val('');
        this.setProcessing(true);

        // Add user message to chat
        this.addMessage(message, 'user');

        // Show typing indicator
        this.showTypingIndicator();

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });

            const data = await response.json();

            // Remove typing indicator
            this.hideTypingIndicator();

            if (response.ok) {
                this.addMessage(data.response, 'bot', data.timestamp);
            } else {
                this.showError(data.error || 'An error occurred while processing your message.');
            }
        } catch (error) {
            console.error('Error sending message:', error);
            this.hideTypingIndicator();
            this.showError('Network error. Please check your connection and try again.');
        } finally {
            this.setProcessing(false);
            this.focusInput();
        }
    }

    async uploadFile(file) {
        if (file.size > 16 * 1024 * 1024) {
            this.showError('File size must be less than 16MB.');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        // Show upload modal
        const uploadModal = new bootstrap.Modal(document.getElementById('uploadModal'));
        uploadModal.show();

        // Simulate progress
        this.simulateUploadProgress();

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            uploadModal.hide();

            if (response.ok) {
                this.showSuccess(`Successfully uploaded and processed: ${file.name}`);
                this.addMessage(`📄 Uploaded and processed: ${file.name}`, 'system');
            } else {
                this.showError(data.error || 'Failed to upload file.');
            }
        } catch (error) {
            console.error('Error uploading file:', error);
            uploadModal.hide();
            this.showError('Network error during file upload.');
        }

        // Reset file input
        $('#pdfUpload').val('');
    }

    simulateUploadProgress() {
        const progressBar = $('.progress-bar');
        let progress = 0;
        
        const interval = setInterval(() => {
            progress += Math.random() * 15;
            if (progress > 90) progress = 90;
            
            progressBar.css('width', progress + '%');
            
            if (progress >= 90) {
                clearInterval(interval);
            }
        }, 200);
    }

    async clearSession() {
        if (!confirm('Are you sure you want to clear the current session? This will remove all conversation history.')) {
            return;
        }

        try {
            const response = await fetch('/clear_session', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            const data = await response.json();

            if (response.ok) {
                // Clear chat messages except welcome message
                const chatMessages = $('#chatMessages');
                chatMessages.find('.message:not(:first)').remove();
                
                this.showSuccess('Session cleared successfully.');
                this.messageCount = 0;
            } else {
                this.showError(data.error || 'Failed to clear session.');
            }
        } catch (error) {
            console.error('Error clearing session:', error);
            this.showError('Network error while clearing session.');
        }
    }

    addMessage(content, type, timestamp = null) {
        const chatMessages = $('#chatMessages');
        const messageId = `message-${++this.messageCount}`;
        const time = timestamp ? new Date(timestamp).toLocaleTimeString() : new Date().toLocaleTimeString();

        let messageHtml = '';

        if (type === 'user') {
            messageHtml = `
                <div class="message user-message" id="${messageId}">
                    <div class="d-flex justify-content-end">
                        <div class="message-content">
                            ${this.formatMessage(content)}
                            <div class="message-time text-end mt-1">
                                <small>${time}</small>
                            </div>
                        </div>
                        <div class="message-avatar user-avatar ms-2">
                            <i class="fas fa-user"></i>
                        </div>
                    </div>
                </div>
            `;
        } else if (type === 'bot') {
            messageHtml = `
                <div class="message bot-message" id="${messageId}">
                    <div class="d-flex">
                        <div class="message-avatar bot-avatar me-2">
                            <i class="fas fa-robot"></i>
                        </div>
                        <div class="flex-grow-1">
                            <div class="message-content">
                                ${this.formatMessage(content)}
                            </div>
                            <div class="message-time mt-1">
                                <small class="text-muted">${time}</small>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        } else if (type === 'system') {
            messageHtml = `
                <div class="message system-message text-center" id="${messageId}">
                    <div class="badge bg-info text-dark">
                        <i class="fas fa-info-circle me-1"></i>
                        ${content}
                    </div>
                </div>
            `;
        }

        chatMessages.append(messageHtml);
        this.scrollToBottom();
    }

    formatMessage(content) {
        // Convert URLs to links
        content = content.replace(/(https?:\/\/[^\s]+)/g, '<a href="$1" target="_blank" rel="noopener">$1</a>');
        
        // Format citations (assuming format: [Source: filename.pdf, Page: X])
        content = content.replace(/\[Source: ([^,]+), Page: (\d+)\]/g, 
            '<div class="citation mt-2"><span class="citation-source">📄 $1</span> - Page $2</div>');
        
        // Convert line breaks to HTML
        content = content.replace(/\n/g, '<br>');
        
        // Format bold text
        content = content.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        
        // Format italic text
        content = content.replace(/\*(.*?)\*/g, '<em>$1</em>');
        
        return content;
    }

    showTypingIndicator() {
        const typingHtml = `
            <div class="message bot-message typing-indicator" id="typing-indicator">
                <div class="d-flex">
                    <div class="message-avatar bot-avatar me-2">
                        <i class="fas fa-robot"></i>
                    </div>
                    <div class="message-content">
                        <div class="typing-dots">
                            <div class="typing-dot"></div>
                            <div class="typing-dot"></div>
                            <div class="typing-dot"></div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        $('#chatMessages').append(typingHtml);
        this.scrollToBottom();
    }

    hideTypingIndicator() {
        $('#typing-indicator').remove();
    }

    setProcessing(processing) {
        this.isProcessing = processing;
        const sendButton = $('#sendButton');
        const messageInput = $('#messageInput');

        if (processing) {
            sendButton.prop('disabled', true).addClass('btn-loading');
            messageInput.prop('disabled', true);
            $('#status-indicator').removeClass('bg-success').addClass('bg-warning').text('Processing...');
        } else {
            sendButton.prop('disabled', false).removeClass('btn-loading');
            messageInput.prop('disabled', false);
            $('#status-indicator').removeClass('bg-warning').addClass('bg-success').text('Online');
        }
    }

    focusInput() {
        setTimeout(() => {
            $('#messageInput').focus();
        }, 100);
    }

    scrollToBottom() {
        const chatMessages = $('#chatMessages');
        chatMessages.scrollTop(chatMessages[0].scrollHeight);
    }

    showError(message) {
        this.showToast(message, 'error');
    }

    showSuccess(message) {
        this.showToast(message, 'success');
    }

    showToast(message, type = 'info') {
        const toastClass = type === 'error' ? 'bg-danger' : type === 'success' ? 'bg-success' : 'bg-info';
        const icon = type === 'error' ? 'fa-exclamation-triangle' : type === 'success' ? 'fa-check-circle' : 'fa-info-circle';
        
        const toastHtml = `
            <div class="toast align-items-center text-white ${toastClass} border-0" role="alert" aria-live="assertive" aria-atomic="true">
                <div class="d-flex">
                    <div class="toast-body">
                        <i class="fas ${icon} me-2"></i>
                        ${message}
                    </div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
                </div>
            </div>
        `;

        // Create toast container if it doesn't exist
        if (!$('#toast-container').length) {
            $('body').append('<div id="toast-container" class="toast-container position-fixed top-0 end-0 p-3"></div>');
        }

        const $toast = $(toastHtml);
        $('#toast-container').append($toast);
        
        const toast = new bootstrap.Toast($toast[0], { delay: 5000 });
        toast.show();

        // Remove toast element after it's hidden
        $toast.on('hidden.bs.toast', function() {
            $(this).remove();
        });
    }

    async checkHealth() {
        try {
            const response = await fetch('/health');
            const data = await response.json();
            
            if (data.status === 'healthy') {
                $('#status-indicator').removeClass('bg-danger bg-warning').addClass('bg-success').text('Online');
            } else {
                $('#status-indicator').removeClass('bg-success bg-warning').addClass('bg-danger').text('Offline');
            }
        } catch (error) {
            console.error('Health check failed:', error);
            $('#status-indicator').removeClass('bg-success bg-warning').addClass('bg-danger').text('Offline');
        }
    }
}

// Initialize the chatbot when the document is ready
$(document).ready(function() {
    window.chatbot = new MedicalChatbot();
    
    // Periodic health check
    setInterval(() => {
        window.chatbot.checkHealth();
    }, 30000); // Check every 30 seconds
});

// Handle page visibility changes
document.addEventListener('visibilitychange', function() {
    if (!document.hidden && window.chatbot) {
        window.chatbot.checkHealth();
    }
});