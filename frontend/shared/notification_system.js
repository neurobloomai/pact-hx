/**
 * PACT Notification System
 * ========================
 * 
 * Real-time notification system for PACT educational interfaces.
 * Provides consistent, accessible, and engaging user feedback across all components.
 */

class PACTNotificationManager {
    constructor(options = {}) {
        this.options = {
            position: options.position || 'top-right',
            maxNotifications: options.maxNotifications || 5,
            defaultDuration: options.defaultDuration || 5000,
            animationDuration: options.animationDuration || 300,
            enableSound: options.enableSound || false,
            enableVibration: options.enableVibration || false,
            debugMode: options.debugMode || false,
            ...options
        };
        
        this.notifications = [];
        this.container = null;
        this.notificationId = 0;
        this.soundEnabled = this.options.enableSound && 'Audio' in window;
        this.vibrationEnabled = this.options.enableVibration && 'vibrate' in navigator;
        
        this.init();
    }
    
    init() {
        this.createContainer();
        this.loadSounds();
        this.setupKeyboardShortcuts();
        
        this.log('🔔 Notification system initialized');
    }
    
    createContainer() {
        // Remove existing container if present
        const existing = document.getElementById('pact-notifications');
        if (existing) {
            existing.remove();
        }
        
        this.container = document.createElement('div');
        this.container.id = 'pact-notifications';
        this.container.className = `pact-notification-container ${this.options.position}`;
        
        // Add CSS styles
        this.injectStyles();
        
        document.body.appendChild(this.container);
    }
    
    injectStyles() {
        const styleId = 'pact-notification-styles';
        
        if (document.getElementById(styleId)) {
            return; // Styles already injected
        }
        
        const style = document.createElement('style');
        style.id = styleId;
        style.textContent = this.getNotificationCSS();
        
        document.head.appendChild(style);
    }
    
    getNotificationCSS() {
        return `
            .pact-notification-container {
                position: fixed;
                z-index: 10000;
                pointer-events: none;
                max-width: 400px;
                width: 100%;
            }
            
            .pact-notification-container.top-right {
                top: 20px;
                right: 20px;
            }
            
            .pact-notification-container.top-left {
                top: 20px;
                left: 20px;
            }
            
            .pact-notification-container.bottom-right {
                bottom: 20px;
                right: 20px;
            }
            
            .pact-notification-container.bottom-left {
                bottom: 20px;
                left: 20px;
            }
            
            .pact-notification-container.top-center {
                top: 20px;
                left: 50%;
                transform: translateX(-50%);
            }
            
            .pact-notification {
                background: #ffffff;
                border-radius: 8px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
                margin-bottom: 10px;
                padding: 16px;
                pointer-events: auto;
                position: relative;
                overflow: hidden;
                transition: all 0.3s ease;
                border-left: 4px solid #3498db;
                min-height: 60px;
                display: flex;
                align-items: center;
            }
            
            .pact-notification.success {
                border-left-color: #27ae60;
                background: linear-gradient(135deg, #d5f4e6 0%, #ffffff 100%);
            }
            
            .pact-notification.warning {
                border-left-color: #f39c12;
                background: linear-gradient(135deg, #fff3cd 0%, #ffffff 100%);
            }
            
            .pact-notification.error {
                border-left-color: #e74c3c;
                background: linear-gradient(135deg, #f8d7da 0%, #ffffff 100%);
            }
            
            .pact-notification.info {
                border-left-color: #17a2b8;
                background: linear-gradient(135deg, #d1ecf1 0%, #ffffff 100%);
            }
            
            .pact-notification.adaptation {
                border-left-color: #9b59b6;
                background: linear-gradient(135deg, #e8daef 0%, #ffffff 100%);
            }
            
            .pact-notification.achievement {
                border-left-color: #f39c12;
                background: linear-gradient(135deg, #fff9c4 0%, #ffffff 100%);
            }
            
            .pact-notification-icon {
                font-size: 24px;
                margin-right: 12px;
                min-width: 30px;
                text-align: center;
            }
            
            .pact-notification-content {
                flex: 1;
            }
            
            .pact-notification-title {
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 4px;
                font-size: 14px;
            }
            
            .pact-notification-message {
                color: #7f8c8d;
                font-size: 13px;
                line-height: 1.4;
            }
            
            .pact-notification-actions {
                margin-top: 8px;
                display: flex;
                gap: 8px;
            }
            
            .pact-notification-btn {
                background: transparent;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                padding: 4px 8px;
                font-size: 12px;
                cursor: pointer;
                transition: all 0.2s ease;
            }
            
            .pact-notification-btn:hover {
                background: #ecf0f1;
            }
            
            .pact-notification-btn.primary {
                background: #3498db;
                color: white;
                border-color: #3498db;
            }
            
            .pact-notification-btn.primary:hover {
                background: #2980b9;
            }
            
            .pact-notification-close {
                position: absolute;
                top: 8px;
                right: 8px;
                background: none;
                border: none;
                font-size: 18px;
                cursor: pointer;
                color: #95a5a6;
                width: 20px;
                height: 20px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 50%;
                transition: all 0.2s ease;
            }
            
            .pact-notification-close:hover {
                background: #ecf0f1;
                color: #7f8c8d;
            }
            
            .pact-notification-progress {
                position: absolute;
                bottom: 0;
                left: 0;
                height: 3px;
                background: #3498db;
                transition: width linear;
            }
            
            .pact-notification.success .pact-notification-progress {
                background: #27ae60;
            }
            
            .pact-notification.warning .pact-notification-progress {
                background: #f39c12;
            }
            
            .pact-notification.error .pact-notification-progress {
                background: #e74c3c;
            }
            
            .pact-notification-enter {
                animation: slideIn 0.3s ease-out;
            }
            
            .pact-notification-exit {
                animation: slideOut 0.3s ease-in;
            }
            
            @keyframes slideIn {
                from {
                    transform: translateX(100%);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }
            
            @keyframes slideOut {
                from {
                    transform: translateX(0);
                    opacity: 1;
                }
                to {
                    transform: translateX(100%);
                    opacity: 0;
                }
            }
            
            @media (max-width: 768px) {
                .pact-notification-container {
                    left: 10px !important;
                    right: 10px !important;
                    max-width: none;
                    transform: none !important;
                }
                
                .pact-notification {
                    margin-bottom: 8px;
                    padding: 12px;
                }
            }
        `;
    }
    
    loadSounds() {
        if (!this.soundEnabled) return;
        
        this.sounds = {
            success: this.createAudioElement('data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmwhDkCazvLCZiALOIjP9rtoGww2jdvmyGkbDTiS1/PCZh4KOI/U77FgGQ02k9j3xm4hCz6RzvHMeSsFJXfH8N+UQAsTYrPr77djIQo1jdvn1GkeEU9a7/X9kh5NJuHJ7cJiHhVJvubV+ocSSkr0/4d5kVWKmOXFLTF2wOl1s18j0Q=='),
            warning: this.createAudioElement('data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmwhDkCazvLCZiALOIjP9rtoGww2jdvmyGkbDTiS1/PCZh4KOI/U77FgGQ02k9j3xm4hCz6RzvHMeSsFJXfH8N+UQAsTYrPr77djIQo1jdvn1GkeEU9a7/X9kh5NJuHJ7cJiHhVJvubV+ocSSkr0/4d5kVWKmOXFLTF2wOl1s18j0Q=='),
            error: this.createAudioElement('data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmwhDkCazvLCZiALOIjP9rtoGww2jdvmyGkbDTiS1/PCZh4KOI/U77FgGQ02k9j3xm4hCz6RzvHMeSsFJXfH8N+UQAsTYrPr77djIQo1jdvn1GkeEU9a7/X9kh5NJuHJ7cJiHhVJvubV+ocSSkr0/4d5kVWKmOXFLTF2wOl1s18j0Q=='),
            info: this.createAudioElement('data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmwhDkCazvLCZiALOIjP9rtoGww2jdvmyGkbDTiS1/PCZh4KOI/U77FgGQ02k9j3xm4hCz6RzvHMeSsFJXfH8N+UQAsTYrPr77djIQo1jdvn1GkeEU9a7/X9kh5NJuHJ7cJiHhVJvubV+ocSSkr0/4d5kVWKmOXFLTF2wOl1s18j0Q==')
        };
    }
    
    createAudioElement(src) {
        const audio = new Audio(src);
        audio.volume = 0.3;
        return audio;
    }
    
    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Escape key to dismiss all notifications
            if (e.key === 'Escape' && this.notifications.length > 0) {
                this.dismissAll();
                e.preventDefault();
            }
        });
    }
    
    // Main notification methods
    show(message, type = 'info', options = {}) {
        const notification = this.createNotification(message, type, options);
        this.addNotification(notification);
        return notification;
    }
    
    success(message, options = {}) {
        return this.show(message, 'success', options);
    }
    
    warning(message, options = {}) {
        return this.show(message, 'warning', options);
    }
    
    error(message, options = {}) {
        return this.show(message, 'error', { duration: 0, ...options }); // Errors don't auto-dismiss
    }
    
    info(message, options = {}) {
        return this.show(message, 'info', options);
    }
    
    adaptation(title, message, options = {}) {
        return this.show(message, 'adaptation', { 
            title: title || '⚡ Content Adapted',
            ...options 
        });
    }
    
    achievement(title, message, options = {}) {
        return this.show(message, 'achievement', { 
            title: title || '🏆 Achievement Unlocked',
            ...options 
        });
    }
    
    // Specialized educational notifications
    learningProgress(progressData, options = {}) {
        const { tasksCompleted, totalTasks, level } = progressData;
        const percentage = Math.round((tasksCompleted / totalTasks) * 100);
        
        return this.show(
            `You've completed ${tasksCompleted} of ${totalTasks} tasks (${percentage}%)`,
            'success',
            {
                title: `📈 Progress Update - ${level}`,
                actions: [
                    { text: 'View Details', action: () => this.emit('viewProgress', progressData) }
                ],
                ...options
            }
        );
    }
    
    engagementAlert(engagementLevel, options = {}) {
        let type, title, message;
        
        if (engagementLevel < 0.3) {
            type = 'warning';
            title = '😴 Low Engagement Detected';
            message = 'Try interacting with the content or take a short break!';
        } else if (engagementLevel > 0.8) {
            type = 'success';
            title = '🌟 High Engagement!';
            message = 'You\'re doing great! Keep up the excellent work!';
        } else {
            return null; // No notification needed for medium engagement
        }
        
        return this.show(message, type, { title, ...options });
    }
    
    adaptationNotification(adaptationType, reasoning, options = {}) {
        const adaptationMessages = {
            'engagement_drop': {
                title: '🚀 Content Boost',
                message: 'Added interactive elements to re-engage you!'
            },
            'confusion_detected': {
                title: '💡 Extra Help',
                message: 'Provided additional examples and explanations.'
            },
            'mastery_achieved': {
                title: '🎯 Challenge Mode',
                message: 'Unlocked advanced content - you\'re ready!'
            }
        };
        
        const config = adaptationMessages[adaptationType] || {
            title: '⚡ Content Adapted',
            message: reasoning
        };
        
        return this.adaptation(config.title, config.message, {
            actions: [
                { text: 'Got it!', action: (notification) => this.dismiss(notification.id) }
            ],
            ...options
        });
    }
    
    teacherAlert(studentName, alertType, data = {}, options = {}) {
        const alertConfigs = {
            'student_struggling': {
                type: 'warning',
                title: `😰 ${studentName} needs help`,
                message: `Engagement dropped to ${Math.round(data.engagement * 100)}%`,
                actions: [
                    { text: 'Assist Student', action: () => this.emit('assistStudent', { studentName, data }) },
                    { text: 'View Details', action: () => this.emit('viewStudent', { studentName }) }
                ]
            },
            'student_excelling': {
                type: 'success',
                title: `🌟 ${studentName} is excelling`,
                message: `High engagement (${Math.round(data.engagement * 100)}%) and progress`,
                actions: [
                    { text: 'Give Challenge', action: () => this.emit('challengeStudent', { studentName }) }
                ]
            },
            'adaptation_triggered': {
                type: 'info',
                title: `⚡ ${studentName} - Content Adapted`,
                message: data.reasoning || 'Learning experience modified',
                actions: [
                    { text: 'View Adaptation', action: () => this.emit('viewAdaptation', { studentName, data }) }
                ]
            }
        };
        
        const config = alertConfigs[alertType];
        if (!config) return null;
        
        return this.show(config.message, config.type, {
            title: config.title,
            actions: config.actions,
            duration: alertType === 'student_struggling' ? 0 : this.options.defaultDuration,
            ...options
        });
    }
    
    createNotification(message, type, options) {
        const id = ++this.notificationId;
        const notification = {
            id,
            message,
            type,
            title: options.title || this.getDefaultTitle(type),
            duration: options.duration !== undefined ? options.duration : this.options.defaultDuration,
            actions: options.actions || [],
            persistent: options.persistent || false,
            priority: options.priority || 'normal',
            metadata: options.metadata || {},
            createdAt: Date.now(),
            element: null
        };
        
        notification.element = this.createNotificationElement(notification);
        return notification;
    }
    
    getDefaultTitle(type) {
        const titles = {
            'success': '✅ Success',
            'warning': '⚠️ Warning',
            'error': '❌ Error',
            'info': '💡 Information',
            'adaptation': '⚡ Adaptation',
            'achievement': '🏆 Achievement'
        };
        return titles[type] || '📝 Notification';
    }
    
    createNotificationElement(notification) {
        const element = document.createElement('div');
        element.className = `pact-notification ${notification.type} pact-notification-enter`;
        element.setAttribute('data-notification-id', notification.id);
        
        const icon = this.getIcon(notification.type);
        
        let actionsHtml = '';
        if (notification.actions.length > 0) {
            actionsHtml = `
                <div class="pact-notification-actions">
                    ${notification.actions.map((action, index) => `
                        <button class="pact-notification-btn ${action.primary ? 'primary' : ''}" 
                                data-action-index="${index}">
                            ${action.text}
                        </button>
                    `).join('')}
                </div>
            `;
        }
        
        let progressHtml = '';
        if (notification.duration > 0) {
            progressHtml = `<div class="pact-notification-progress" data-duration="${notification.duration}"></div>`;
        }
        
        element.innerHTML = `
            <div class="pact-notification-icon">${icon}</div>
            <div class="pact-notification-content">
                <div class="pact-notification-title">${notification.title}</div>
                <div class="pact-notification-message">${notification.message}</div>
                ${actionsHtml}
            </div>
            <button class="pact-notification-close" aria-label="Close notification">×</button>
            ${progressHtml}
        `;
        
        this.attachEventListeners(element, notification);
        return element;
    }
    
    getIcon(type) {
        const icons = {
            'success': '✅',
            'warning': '⚠️',
            'error': '❌',
            'info': '💡',
            'adaptation': '⚡',
            'achievement': '🏆'
        };
        return icons[type] || '📝';
    }
    
    attachEventListeners(element, notification) {
        // Close button
        const closeBtn = element.querySelector('.pact-notification-close');
        closeBtn.addEventListener('click', () => {
            this.dismiss(notification.id);
        });
        
        // Action buttons
        const actionBtns = element.querySelectorAll('.pact-notification-btn');
        actionBtns.forEach((btn, index) => {
            btn.addEventListener('click', () => {
                const action = notification.actions[index];
                if (action && typeof action.action === 'function') {
                    action.action(notification);
                }
                
                // Auto-dismiss unless action specifies otherwise
                if (action.dismissOnClick !== false) {
                    this.dismiss(notification.id);
                }
            });
        });
        
        // Click to dismiss (optional)
        if (notification.clickToDismiss !== false) {
            element.addEventListener('click', (e) => {
                // Don't dismiss if clicking on action buttons or close button
                if (!e.target.closest('.pact-notification-btn, .pact-notification-close')) {
                    this.dismiss(notification.id);
                }
            });
        }
    }
    
    addNotification(notification) {
        // Remove oldest notifications if at max capacity
        while (this.notifications.length >= this.options.maxNotifications) {
            const oldest = this.notifications[0];
            this.dismiss(oldest.id, false);
        }
        
        this.notifications.push(notification);
        this.container.appendChild(notification.element);
        
        // Play sound if enabled
        this.playSound(notification.type);
        
        // Trigger vibration if enabled
        this.triggerVibration(notification.type);
        
        // Set up auto-dismiss timer
        if (notification.duration > 0) {
            this.setupProgressBar(notification);
            notification.timeoutId = setTimeout(() => {
                this.dismiss(notification.id);
            }, notification.duration);
        }
        
        // Emit event
        this.emit('notificationShown', notification);
        
        this.log(`📢 Notification shown: ${notification.type} - ${notification.title}`);
    }
    
    setupProgressBar(notification) {
        const progressBar = notification.element.querySelector('.pact-notification-progress');
        if (progressBar) {
            progressBar.style.width = '100%';
            progressBar.style.transition = `width ${notification.duration}ms linear`;
            
            // Start the progress animation
            setTimeout(() => {
                progressBar.style.width = '0%';
            }, 10);
        }
    }
    
    dismiss(notificationId, animate = true) {
        const index = this.notifications.findIndex(n => n.id === notificationId);
        if (index === -1) return;
        
        const notification = this.notifications[index];
        
        // Clear timeout if exists
        if (notification.timeoutId) {
            clearTimeout(notification.timeoutId);
        }
        
        if (animate) {
            notification.element.classList.add('pact-notification-exit');
            setTimeout(() => {
                this.removeNotification(index);
            }, this.options.animationDuration);
        } else {
            this.removeNotification(index);
        }
        
        this.emit('notificationDismissed', notification);
        this.log(`📤 Notification dismissed: ${notification.id}`);
    }
    
    removeNotification(index) {
        const notification = this.notifications[index];
        if (notification.element.parentNode) {
            notification.element.parentNode.removeChild(notification.element);
        }
        this.notifications.splice(index, 1);
    }
    
    dismissAll() {
        const notificationIds = this.notifications.map(n => n.id);
        notificationIds.forEach(id => this.dismiss(id, false));
        this.log('📤 All notifications dismissed');
    }
    
    update(notificationId, updates) {
        const notification = this.notifications.find(n => n.id === notificationId);
        if (!notification) return;
        
        Object.assign(notification, updates);
        
        // Update the DOM element
        if (updates.title) {
            const titleElement = notification.element.querySelector('.pact-notification-title');
            if (titleElement) titleElement.textContent = updates.title;
        }
        
        if (updates.message) {
            const messageElement = notification.element.querySelector('.pact-notification-message');
            if (messageElement) messageElement.textContent = updates.message;
        }
        
        if (updates.type) {
            notification.element.className = notification.element.className.replace(
                /pact-notification-\w+/g, 
                `pact-notification-${updates.type}`
            );
        }
        
        this.log(`📝 Notification updated: ${notificationId}`);
    }
    
    // Sound and vibration
    playSound(type) {
        if (!this.soundEnabled || !this.sounds[type]) return;
        
        try {
            this.sounds[type].currentTime = 0;
            this.sounds[type].play().catch(e => {
                // Ignore autoplay restrictions
                this.log(`🔇 Sound play failed: ${e.message}`);
            });
        } catch (error) {
            this.log(`🔇 Sound error: ${error.message}`);
        }
    }
    
    triggerVibration(type) {
        if (!this.vibrationEnabled) return;
        
        const patterns = {
            'success': [100, 50, 100],
            'warning': [200, 100, 200],
            'error': [300, 100, 300, 100, 300],
            'info': [100],
            'adaptation': [150, 50, 150],
            'achievement': [100, 50, 100, 50, 200]
        };
        
        const pattern = patterns[type] || [100];
        navigator.vibrate(pattern);
    }
    
    // Event system
    on(eventType, callback) {
        if (!this.eventListeners) {
            this.eventListeners = {};
        }
        
        if (!this.eventListeners[eventType]) {
            this.eventListeners[eventType] = [];
        }
        
        this.eventListeners[eventType].push(callback);
        
        return () => this.off(eventType, callback);
    }
    
    off(eventType, callback) {
        if (this.eventListeners && this.eventListeners[eventType]) {
            const index = this.eventListeners[eventType].indexOf(callback);
            if (index > -1) {
                this.eventListeners[eventType].splice(index, 1);
            }
        }
    }
    
    emit(eventType, data) {
        if (this.eventListeners && this.eventListeners[eventType]) {
            this.eventListeners[eventType].forEach(callback => {
                try {
                    callback(data);
                } catch (error) {
                    this.log(`❌ Event callback error: ${error.message}`);
                }
            });
        }
    }
    
    // Utility methods
    getNotifications(type = null) {
        if (type) {
            return this.notifications.filter(n => n.type === type);
        }
        return [...this.notifications];
    }
    
    hasNotifications(type = null) {
        return this.getNotifications(type).length > 0;
    }
    
    clear(type = null) {
        if (type) {
            const toRemove = this.notifications.filter(n => n.type === type);
            toRemove.forEach(n => this.dismiss(n.id, false));
        } else {
            this.dismissAll();
        }
    }
    
    setPosition(position) {
        this.options.position = position;
        this.container.className = `pact-notification-container ${position}`;
    }
    
    setMaxNotifications(max) {
        this.options.maxNotifications = max;
        
        // Remove excess notifications if needed
        while (this.notifications.length > max) {
            const oldest = this.notifications[0];
            this.dismiss(oldest.id, false);
        }
    }
    
    enableSounds(enabled = true) {
        this.options.enableSound = enabled && 'Audio' in window;
        this.soundEnabled = this.options.enableSound;
    }
    
    enableVibration(enabled = true) {
        this.options.enableVibration = enabled && 'vibrate' in navigator;
        this.vibrationEnabled = this.options.enableVibration;
    }
    
    destroy() {
        this.dismissAll();
        
        if (this.container && this.container.parentNode) {
            this.container.parentNode.removeChild(this.container);
        }
        
        // Remove styles
        const styles = document.getElementById('pact-notification-styles');
        if (styles) {
            styles.remove();
        }
        
        this.log('🗑️ Notification system destroyed');
    }
    
    log(...args) {
        if (this.options.debugMode) {
            console.log('[PACT Notifications]', ...args);
        }
    }
}

// Specialized notification managers for different contexts
class StudentNotificationManager extends PACTNotificationManager {
    constructor(options = {}) {
        super({
            position: 'top-right',
            enableSound: true,
            enableVibration: true,
            ...options
        });
    }
    
    showLearningHint(hint, options = {}) {
        return this.info(hint, {
            title: '💡 Learning Hint',
            actions: [
                { text: 'Got it!', action: (notification) => this.dismiss(notification.id) },
                { text: 'More hints', action: () => this.emit('requestMoreHints') }
            ],
            ...options
        });
    }
    
    celebrateSuccess(achievement, options = {}) {
        return this.achievement('🎉 Well Done!', achievement, {
            duration: 7000,
            actions: [
                { text: 'Continue Learning', action: () => this.emit('continueeLearning') }
            ],
            ...options
        });
    }
    
    encourageStruggling(message, options = {}) {
        return this.warning(message || "Don't worry, learning takes time! Try a different approach.", {
            title: '💪 Keep Going!',
            actions: [
                { text: 'Get Help', action: () => this.emit('requestHelp') },
                { text: 'Try Again', action: () => this.emit('tryAgain') }
            ],
            ...options
        });
    }
}

class TeacherNotificationManager extends PACTNotificationManager {
    constructor(options = {}) {
        super({
            position: 'top-left',
            maxNotifications: 8,
            enableSound: true,
            ...options
        });
    }
    
    studentNeedsAttention(studentName, details, options = {}) {
        return this.teacherAlert(studentName, 'student_struggling', details, {
            persistent: true,
            priority: 'high',
            ...options
        });
    }
    
    classroomUpdate(message, data = {}, options = {}) {
        return this.info(message, {
            title: '📊 Classroom Update',
            metadata: data,
            ...options
        });
    }
    
    adaptationAlert(studentName, adaptationType, reasoning, options = {}) {
        return this.teacherAlert(studentName, 'adaptation_triggered', { 
            adaptationType, 
            reasoning 
        }, options);
    }
}

// Factory function
function createNotificationManager(type = 'general', options = {}) {
    switch (type) {
        case 'student':
            return new StudentNotificationManager(options);
        case 'teacher':
            return new TeacherNotificationManager(options);
        default:
            return new PACTNotificationManager(options);
    }
}

// Global notification manager
let globalNotificationManager = null;

function getGlobalNotificationManager(type = 'general', options = {}) {
    if (!globalNotificationManager) {
        globalNotificationManager = createNotificationManager(type, {
            debugMode: true,
            ...options
        });
    }
    return globalNotificationManager;
}

// Convenience functions
function notify(message, type = 'info', options = {}) {
    const manager = getGlobalNotificationManager();
    return manager.show(message, type, options);
}

function notifySuccess(message, options = {}) {
    return notify(message, 'success', options);
}

function notifyWarning(message, options = {}) {
    return notify(message, 'warning', options);
}

function notifyError(message, options = {}) {
    return notify(message, 'error', options);
}

function notifyInfo(message, options = {}) {
    return notify(message, 'info', options);
}

// Export for different environments
if (typeof window !== 'undefined') {
    // Browser environment
    window.PACTNotificationManager = PACTNotificationManager;
    window.StudentNotificationManager = StudentNotificationManager;
    window.TeacherNotificationManager = TeacherNotificationManager;
    window.createNotificationManager = createNotificationManager;
    window.getGlobalNotificationManager = getGlobalNotificationManager;
    
    // Convenience functions
    window.notify = notify;
    window.notifySuccess = notifySuccess;
    window.notifyWarning = notifyWarning;
    window.notifyError = notifyError;
    window.notifyInfo = notifyInfo;
}

if (typeof module !== 'undefined' && module.exports) {
    // Node.js environment
    module.exports = {
        PACTNotificationManager,
        StudentNotificationManager,
        TeacherNotificationManager,
        createNotificationManager
    };
}
