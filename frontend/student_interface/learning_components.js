/**
 * PACT Learning Components
 * ========================
 * 
 * Interactive learning elements that adapt to student behavior and learning styles.
 * Provides engaging educational activities with real-time feedback and adaptation.
 */

class LearningComponentManager {
    constructor(config = {}) {
        this.config = {
            apiEndpoint: config.apiEndpoint || 'http://localhost:5000',
            adaptationEnabled: config.adaptationEnabled || true,
            debugMode: config.debugMode || false,
            ...config
        };
        
        this.currentExperience = null;
        this.studentProfile = null;
        this.componentInstances = new Map();
        this.eventListeners = [];
        
        this.init();
    }
    
    init() {
        this.log('🎮 Learning Components Manager initializing...');
        this.setupEventListeners();
        this.log('✅ Learning Components ready');
    }
    
    setupEventListeners() {
        // Listen for experience updates
        document.addEventListener('experienceGenerated', (event) => {
            this.loadExperience(event.detail.experience);
        });
        
        // Listen for adaptations
        document.addEventListener('adaptationApplied', (event) => {
            this.applyAdaptation(event.detail.adaptation);
        });
    }
    
    setStudentProfile(profile) {
        this.studentProfile = profile;
        this.log(`👨‍🎓 Student profile set: ${profile.name} (${profile.learning_style})`);
    }
    
    loadExperience(experience) {
        this.currentExperience = experience;
        this.log(`📚 Loading experience: ${experience.experience_id}`);
        
        // Clear existing components
        this.clearComponents();
        
        // Render new components based on experience content
        this.renderExperienceComponents(experience);
    }
    
    clearComponents() {
        // Remove all active learning components
        this.componentInstances.forEach((component, id) => {
            if (component.destroy) {
                component.destroy();
            }
        });
        this.componentInstances.clear();
        
        // Clear the learning content area
        const container = document.getElementById('learningContent');
        if (container) {
            container.innerHTML = '';
        }
    }
    
    renderExperienceComponents(experience) {
        const container = document.getElementById('learningContent');
        if (!container) {
            this.log('❌ Learning content container not found');
            return;
        }
        
        const content = experience.content;
        let html = '';
        
        // Render based on learning style
        if (this.studentProfile?.learning_style === 'visual') {
            html += this.renderVisualComponents(content);
        } else if (this.studentProfile?.learning_style === 'kinesthetic') {
            html += this.renderKinestheticComponents(content);
        } else if (this.studentProfile?.learning_style === 'auditory') {
            html += this.renderAuditoryComponents(content);
        } else {
            html += this.renderTextComponents(content);
        }
        
        // Add interactive elements
        html += this.renderInteractiveElements(content);
        
        // Add assessment components
        if (content.knowledge_checks) {
            html += this.renderAssessmentComponents(content.knowledge_checks);
        }
        
        container.innerHTML = html;
        
        // Initialize interactive components
        this.initializeInteractiveComponents();
    }
    
    renderVisualComponents(content) {
        return `
            <div class="visual-learning-section">
                <h2>🎨 ${content.title}</h2>
                
                <div class="visual-objectives">
                    <h3>🎯 What You'll Learn:</h3>
                    <div class="objectives-visual">
                        ${content.learning_objectives?.map(obj => `
                            <div class="objective-card">
                                <div class="objective-icon">📍</div>
                                <div class="objective-text">${obj}</div>
                            </div>
                        `).join('') || ''}
                    </div>
                </div>
                
                <div class="visual-content-area">
                    ${this.createFractionVisualizer()}
                    ${this.createInteractiveDiagram()}
                    ${this.createConceptMap()}
                </div>
            </div>
        `;
    }
    
    renderKinestheticComponents(content) {
        return `
            <div class="kinesthetic-learning-section">
                <h2>🤲 ${content.title}</h2>
                
                <div class="hands-on-activities">
                    <h3>👐 Interactive Activities:</h3>
                    ${this.createDragDropActivity()}
                    ${this.createBuildingBlocks()}
                    ${this.createPhysicalSimulation()}
                </div>
            </div>
        `;
    }
    
    renderAuditoryComponents(content) {
        return `
            <div class="auditory-learning-section">
                <h2>🔊 ${content.title}</h2>
                
                <div class="audio-content">
                    <h3>🎵 Listen and Learn:</h3>
                    ${this.createAudioNarration()}
                    ${this.createRhythmActivity()}
                    ${this.createVoiceInteraction()}
                </div>
            </div>
        `;
    }
    
    renderTextComponents(content) {
        return `
            <div class="text-learning-section">
                <h2>📚 ${content.title}</h2>
                
                <div class="reading-content">
                    <h3>📖 Read and Understand:</h3>
                    ${this.createStructuredText(content)}
                    ${this.createVocabularyBuilder()}
                    ${this.createReadingComprehension()}
                </div>
            </div>
        `;
    }
    
    createFractionVisualizer() {
        return `
            <div class="learning-component fraction-visualizer" data-component="fraction-visualizer">
                <h4>🍕 Interactive Fraction Pizza</h4>
                <div class="pizza-container">
                    <div class="pizza" id="fractionPizza">
                        <div class="pizza-slice" data-slice="1"></div>
                        <div class="pizza-slice" data-slice="2"></div>
                        <div class="pizza-slice" data-slice="3"></div>
                        <div class="pizza-slice" data-slice="4"></div>
                        <div class="pizza-slice" data-slice="5"></div>
                        <div class="pizza-slice" data-slice="6"></div>
                        <div class="pizza-slice" data-slice="7"></div>
                        <div class="pizza-slice" data-slice="8"></div>
                    </div>
                </div>
                <div class="fraction-controls">
                    <button onclick="learningComponents.selectSlices(1)">1/8</button>
                    <button onclick="learningComponents.selectSlices(2)">2/8 = 1/4</button>
                    <button onclick="learningComponents.selectSlices(4)">4/8 = 1/2</button>
                    <button onclick="learningComponents.selectSlices(6)">6/8 = 3/4</button>
                    <button onclick="learningComponents.clearSlices()">Clear</button>
                </div>
                <div class="fraction-display">
                    <span id="fractionDisplay">0/8</span>
                </div>
            </div>
        `;
    }
    
    createDragDropActivity() {
        return `
            <div class="learning-component drag-drop-activity" data-component="drag-drop">
                <h4>🎯 Drag & Drop Fractions</h4>
                <div class="drag-drop-container">
                    <div class="fraction-pieces">
                        <div class="draggable-piece" draggable="true" data-value="1/4">1/4</div>
                        <div class="draggable-piece" draggable="true" data-value="1/2">1/2</div>
                        <div class="draggable-piece" draggable="true" data-value="3/4">3/4</div>
                        <div class="draggable-piece" draggable="true" data-value="1/8">1/8</div>
                    </div>
                    <div class="drop-zones">
                        <div class="drop-zone" data-target="smallest">
                            <span>Smallest</span>
                        </div>
                        <div class="drop-zone" data-target="largest">
                            <span>Largest</span>
                        </div>
                    </div>
                </div>
                <div class="activity-feedback" id="dragDropFeedback"></div>
            </div>
        `;
    }
    
    createAudioNarration() {
        return `
            <div class="learning-component audio-narration" data-component="audio-narration">
                <h4>🎙️ Listen to the Lesson</h4>
                <div class="audio-player">
                    <button class="audio-btn" onclick="learningComponents.playNarration()">
                        ▶️ Play Lesson
                    </button>
                    <button class="audio-btn" onclick="learningComponents.pauseNarration()">
                        ⏸️ Pause
                    </button>
                    <div class="audio-progress">
                        <div class="progress-bar" id="audioProgress"></div>
                    </div>
                </div>
                <div class="audio-transcript" id="audioTranscript">
                    <p><em>Click play to hear the lesson narration...</em></p>
                </div>
            </div>
        `;
    }
    
    renderInteractiveElements(content) {
        return `
            <div class="interactive-elements-section">
                <h3>🎮 Interactive Practice</h3>
                ${this.createProgressTracker()}
                ${this.createHintSystem()}
                ${this.createAchievementDisplay()}
            </div>
        `;
    }
    
    createProgressTracker() {
        return `
            <div class="learning-component progress-tracker" data-component="progress-tracker">
                <h4>📈 Your Progress</h4>
                <div class="progress-container">
                    <div class="progress-ring">
                        <div class="progress-circle" id="progressCircle">
                            <span class="progress-text" id="progressText">0%</span>
                        </div>
                    </div>
                    <div class="progress-details">
                        <div class="progress-item">
                            <span class="progress-label">Tasks Completed:</span>
                            <span class="progress-value" id="tasksCompleted">0/5</span>
                        </div>
                        <div class="progress-item">
                            <span class="progress-label">Understanding Level:</span>
                            <span class="progress-value" id="understandingLevel">Beginner</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }
    
    createHintSystem() {
        return `
            <div class="learning-component hint-system" data-component="hint-system">
                <button class="hint-button" onclick="learningComponents.showHint()">
                    💡 Need a Hint?
                </button>
                <div class="hint-display" id="hintDisplay" style="display: none;">
                    <div class="hint-content">
                        <h5>💡 Helpful Hint:</h5>
                        <p id="hintText">Try breaking the fraction into smaller pieces!</p>
                        <button onclick="learningComponents.hideHint()">Got it! ✓</button>
                    </div>
                </div>
            </div>
        `;
    }
    
    renderAssessmentComponents(knowledgeChecks) {
        return `
            <div class="assessment-section">
                <h3>🧠 Knowledge Check</h3>
                ${knowledgeChecks.map((check, index) => this.createQuizComponent(check, index)).join('')}
            </div>
        `;
    }
    
    createQuizComponent(question, index) {
        if (question.type === 'multiple_choice') {
            return `
                <div class="learning-component quiz-component" data-component="quiz-${index}">
                    <h4>❓ ${question.question}</h4>
                    <div class="quiz-options">
                        <div class="quiz-option" onclick="learningComponents.selectAnswer(${index}, 'A')">
                            A) One quarter of the whole
                        </div>
                        <div class="quiz-option" onclick="learningComponents.selectAnswer(${index}, 'B')">
                            B) One half of the whole
                        </div>
                        <div class="quiz-option" onclick="learningComponents.selectAnswer(${index}, 'C')">
                            C) Three quarters of the whole
                        </div>
                        <div class="quiz-option" onclick="learningComponents.selectAnswer(${index}, 'D')">
                            D) The whole thing
                        </div>
                    </div>
                    <div class="quiz-feedback" id="quizFeedback${index}"></div>
                </div>
            `;
        }
        return '';
    }
    
    initializeInteractiveComponents() {
        // Initialize fraction visualizer
        this.initializeFractionVisualizer();
        
        // Initialize drag and drop
        this.initializeDragDrop();
        
        // Initialize audio components
        this.initializeAudioComponents();
        
        // Initialize progress tracking
        this.initializeProgressTracking();
        
        this.log('🎮 Interactive components initialized');
    }
    
    initializeFractionVisualizer() {
        const component = new FractionVisualizerComponent();
        this.componentInstances.set('fraction-visualizer', component);
    }
    
    initializeDragDrop() {
        const component = new DragDropComponent();
        this.componentInstances.set('drag-drop', component);
    }
    
    initializeAudioComponents() {
        const component = new AudioNarrationComponent();
        this.componentInstances.set('audio-narration', component);
    }
    
    initializeProgressTracking() {
        const component = new ProgressTrackerComponent();
        this.componentInstances.set('progress-tracker', component);
    }
    
    // Public methods for component interactions
    selectSlices(count) {
        const component = this.componentInstances.get('fraction-visualizer');
        if (component) component.selectSlices(count);
    }
    
    clearSlices() {
        const component = this.componentInstances.get('fraction-visualizer');
        if (component) component.clearSlices();
    }
    
    showHint() {
        document.getElementById('hintDisplay').style.display = 'block';
        this.trackInteraction('hint_requested');
    }
    
    hideHint() {
        document.getElementById('hintDisplay').style.display = 'none';
        this.trackInteraction('hint_dismissed');
    }
    
    selectAnswer(questionIndex, answer) {
        const feedback = document.getElementById(`quizFeedback${questionIndex}`);
        const correct = answer === 'A'; // Simplified for demo
        
        if (correct) {
            feedback.innerHTML = '<div class="feedback-correct">✅ Correct! Well done!</div>';
            this.updateProgress();
        } else {
            feedback.innerHTML = '<div class="feedback-incorrect">❌ Not quite. Try again!</div>';
        }
        
        this.trackInteraction('quiz_answer', { question: questionIndex, answer, correct });
    }
    
    playNarration() {
        const component = this.componentInstances.get('audio-narration');
        if (component) component.play();
        this.trackInteraction('audio_play');
    }
    
    pauseNarration() {
        const component = this.componentInstances.get('audio-narration');
        if (component) component.pause();
        this.trackInteraction('audio_pause');
    }
    
    updateProgress() {
        const component = this.componentInstances.get('progress-tracker');
        if (component) component.updateProgress();
    }
    
    trackInteraction(type, data = {}) {
        // Send interaction data to engagement tracker
        if (window.pactTracker) {
            window.pactTracker.trackLearningInteraction(type, data);
        }
        
        // Dispatch custom event
        document.dispatchEvent(new CustomEvent('learningInteraction', {
            detail: { type, data, timestamp: Date.now() }
        }));
        
        this.log(`🎯 Interaction tracked: ${type}`, data);
    }
    
    applyAdaptation(adaptation) {
        this.log(`⚡ Applying adaptation: ${adaptation.adaptation_type}`);
        
        const modified = adaptation.modified_content;
        
        if (modified.content_simplification) {
            this.simplifyContent();
        }
        
        if (modified.interaction_boost) {
            this.addInteractiveElements();
        }
        
        if (modified.additional_examples) {
            this.addExamples();
        }
        
        if (modified.gamification_elements) {
            this.addGamificationElements(modified.gamification_elements);
        }
    }
    
    simplifyContent() {
        // Simplify current components
        const containers = document.querySelectorAll('.learning-component');
        containers.forEach(container => {
            container.classList.add('simplified-mode');
        });
        
        this.log('📝 Content simplified');
    }
    
    addInteractiveElements() {
        // Add more interactive features
        const container = document.getElementById('learningContent');
        if (container) {
            const boostElement = document.createElement('div');
            boostElement.className = 'engagement-boost';
            boostElement.innerHTML = `
                <div class="boost-notification">
                    🚀 New interactive features unlocked!
                    <button onclick="this.parentElement.remove()">✓</button>
                </div>
            `;
            container.insertBefore(boostElement, container.firstChild);
        }
        
        this.log('🎮 Interactive elements added');
    }
    
    addGamificationElements(elements) {
        if (elements.includes('progress_bar')) {
            this.enhanceProgressBar();
        }
        
        if (elements.includes('achievement_badge')) {
            this.showAchievementBadge();
        }
        
        this.log('🏆 Gamification elements added', elements);
    }
    
    enhanceProgressBar() {
        const progressTracker = document.querySelector('.progress-tracker');
        if (progressTracker) {
            progressTracker.classList.add('enhanced');
        }
    }
    
    showAchievementBadge() {
        const badge = document.createElement('div');
        badge.className = 'achievement-badge';
        badge.innerHTML = `
            <div class="badge-content">
                🏆 Achievement Unlocked!
                <div class="badge-title">Persistence Master</div>
                <button onclick="this.parentElement.parentElement.remove()">Claim Reward</button>
            </div>
        `;
        
        document.body.appendChild(badge);
        
        setTimeout(() => {
            if (badge.parentElement) {
                badge.remove();
            }
        }, 5000);
    }
    
    log(...args) {
        if (this.config.debugMode) {
            console.log('[Learning Components]', ...args);
        }
    }
}

// Individual Component Classes
class FractionVisualizerComponent {
    constructor() {
        this.selectedSlices = 0;
        this.totalSlices = 8;
    }
    
    selectSlices(count) {
        this.selectedSlices = count;
        this.updateVisualization();
        this.updateDisplay();
    }
    
    clearSlices() {
        this.selectedSlices = 0;
        this.updateVisualization();
        this.updateDisplay();
    }
    
    updateVisualization() {
        const slices = document.querySelectorAll('.pizza-slice');
        slices.forEach((slice, index) => {
            if (index < this.selectedSlices) {
                slice.classList.add('selected');
            } else {
                slice.classList.remove('selected');
            }
        });
    }
    
    updateDisplay() {
        const display = document.getElementById('fractionDisplay');
        if (display) {
            display.textContent = `${this.selectedSlices}/${this.totalSlices}`;
        }
    }
}

class DragDropComponent {
    constructor() {
        this.setupDragAndDrop();
    }
    
    setupDragAndDrop() {
        const draggables = document.querySelectorAll('.draggable-piece');
        const dropZones = document.querySelectorAll('.drop-zone');
        
        draggables.forEach(draggable => {
            draggable.addEventListener('dragstart', this.handleDragStart);
        });
        
        dropZones.forEach(zone => {
            zone.addEventListener('dragover', this.handleDragOver);
            zone.addEventListener('drop', this.handleDrop);
        });
    }
    
    handleDragStart(e) {
        e.dataTransfer.setData('text/plain', e.target.dataset.value);
        e.target.classList.add('dragging');
    }
    
    handleDragOver(e) {
        e.preventDefault();
        e.target.classList.add('drag-over');
    }
    
    handleDrop(e) {
        e.preventDefault();
        const data = e.dataTransfer.getData('text/plain');
        const feedback = document.getElementById('dragDropFeedback');
        
        // Simple validation logic
        const isCorrect = (e.target.dataset.target === 'smallest' && data === '1/8') ||
                         (e.target.dataset.target === 'largest' && data === '3/4');
        
        if (isCorrect) {
            feedback.innerHTML = '<div class="feedback-correct">✅ Excellent! Correct placement!</div>';
            e.target.innerHTML = `<span>✓ ${data}</span>`;
        } else {
            feedback.innerHTML = '<div class="feedback-incorrect">🤔 Try again! Think about which fraction is bigger.</div>';
        }
        
        e.target.classList.remove('drag-over');
        document.querySelector('.dragging')?.classList.remove('dragging');
    }
}

class AudioNarrationComponent {
    constructor() {
        this.isPlaying = false;
        this.progress = 0;
        this.transcript = [
            "Welcome to learning about fractions!",
            "A fraction represents a part of a whole.",
            "The top number is called the numerator.",
            "The bottom number is called the denominator.",
            "Let's explore fractions with our interactive pizza!"
        ];
        this.currentLine = 0;
    }
    
    play() {
        if (!this.isPlaying) {
            this.isPlaying = true;
            this.startNarration();
        }
    }
    
    pause() {
        this.isPlaying = false;
    }
    
    startNarration() {
        if (!this.isPlaying) return;
        
        const transcriptElement = document.getElementById('audioTranscript');
        const progressBar = document.getElementById('audioProgress');
        
        if (this.currentLine < this.transcript.length) {
            transcriptElement.innerHTML = `<p><strong>🎙️ "${this.transcript[this.currentLine]}"</strong></p>`;
            
            this.progress = (this.currentLine + 1) / this.transcript.length * 100;
            progressBar.style.width = this.progress + '%';
            
            this.currentLine++;
            
            setTimeout(() => {
                if (this.isPlaying) {
                    this.startNarration();
                }
            }, 2000);
        } else {
            this.isPlaying = false;
            this.currentLine = 0;
            transcriptElement.innerHTML = '<p><em>✅ Narration complete! Click play to hear again.</em></p>';
        }
    }
}

class ProgressTrackerComponent {
    constructor() {
        this.tasksCompleted = 0;
        this.totalTasks = 5;
        this.updateDisplay();
    }
    
    updateProgress() {
        this.tasksCompleted = Math.min(this.tasksCompleted + 1, this.totalTasks);
        this.updateDisplay();
    }
    
    updateDisplay() {
        const progressText = document.getElementById('progressText');
        const tasksElement = document.getElementById('tasksCompleted');
        const levelElement = document.getElementById('understandingLevel');
        const progressCircle = document.getElementById('progressCircle');
        
        const percentage = Math.round((this.tasksCompleted / this.totalTasks) * 100);
        
        if (progressText) progressText.textContent = percentage + '%';
        if (tasksElement) tasksElement.textContent = `${this.tasksCompleted}/${this.totalTasks}`;
        
        // Update understanding level
        let level = 'Beginner';
        if (percentage >= 80) level = 'Expert';
        else if (percentage >= 60) level = 'Advanced';
        else if (percentage >= 40) level = 'Intermediate';
        
        if (levelElement) levelElement.textContent = level;
        
        // Update progress circle color
        if (progressCircle) {
            progressCircle.style.background = `conic-gradient(#4caf50 ${percentage * 3.6}deg, #e0e0e0 0deg)`;
        }
    }
}

// Global instance
let learningComponents;

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    learningComponents = new LearningComponentManager({
        debugMode: true,
        adaptationEnabled: true
    });
});

// Export for module use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { LearningComponentManager, FractionVisualizerComponent, DragDropComponent };
}
