import React, { useState, useEffect } from 'react';
import { Calendar, CheckCircle2, Circle, Trophy, Zap, Clock, Book, Target, Star, Flame, Brain, Code, Database, Settings, BarChart3, MessageSquare } from 'lucide-react';

const getAPIConfig = () => {
  // Configuration will be loaded from config.js
  return window.AITrackerConfig || {
    API_URL: 'http://localhost:8000',
    DEBUG: false,
    ENVIRONMENT: 'development'
  };
};

const API_CONFIG = getAPIConfig();
const API_BASE_URL = API_CONFIG.API_URL;

const AIProgressTracker = () => {
  // Core State Management
  const [currentWeek, setCurrentWeek] = useState(1);
  const [currentDay, setCurrentDay] = useState(1);
  const [totalXP, setTotalXP] = useState(0);
  const [dailyXP, setDailyXP] = useState(0);
  const [streak, setStreak] = useState(0);
  const [showCelebration, setShowCelebration] = useState(false);
  const [notes, setNotes] = useState({});
  const [completedTasks, setCompletedTasks] = useState(new Set());
  const [struggledTasks, setStruggleTasks] = useState(new Set());
  
  // Enhanced Features State
  const [spaceRepetitionQueue, setSpaceRepetitionQueue] = useState([]);
  const [difficultyLevel, setDifficultyLevel] = useState('medium');
  const [portfolioItems, setPortfolioItems] = useState([]);
  const [certificationProgress, setCertificationProgress] = useState({
    'Google Cloud AI': 0,
    'AWS ML Specialty': 0,
    'Azure AI Engineer': 0
  });

  // Week 1 Curriculum Data
  const curriculum = {
    1: {
      theme: "Exception Handling for AI Systems",
      description: "Master bulletproof error handling for AI applications",
      learningObjectives: [
        "Understand AI-specific error patterns",
        "Implement robust error recovery systems",
        "Build production-ready error handling",
        "Create monitoring and alerting systems"
      ],
      dailyTasks: {
        1: [
          { id: 'w1d1t1', task: 'Review Python Exception Handling Guide', points: 50, time: 1.0, category: 'foundation', difficulty: 'easy' },
          { id: 'w1d1t2', task: 'Learn AI-Specific Error Patterns', points: 75, time: 1.0, category: 'ai', difficulty: 'medium' },
          { id: 'w1d1t3', task: 'Practice Error Classification Exercise', points: 100, time: 1.0, category: 'practice', difficulty: 'medium' }
        ],
        2: [
          { id: 'w1d2t1', task: 'Fix Broken AI Data Loader', points: 150, time: 1.0, category: 'coding', difficulty: 'medium' },
          { id: 'w1d2t2', task: 'Build Safe Model Prediction Endpoint', points: 200, time: 2.0, category: 'project', difficulty: 'hard' }
        ],
        3: [
          { id: 'w1d3t1', task: 'Build AI Pipeline with Error Recovery', points: 300, time: 3.0, category: 'project', difficulty: 'hard' }
        ],
        4: [
          { id: 'w1d4t1', task: 'Implement Circuit Breaker Pattern', points: 200, time: 2.0, category: 'production', difficulty: 'hard' },
          { id: 'w1d4t2', task: 'Build Error Monitoring System', points: 150, time: 1.0, category: 'monitoring', difficulty: 'medium' }
        ],
        5: [
          { id: 'w1d5t1', task: 'Complete Bulletproof AI Data Processor', points: 500, time: 3.0, category: 'capstone', difficulty: 'expert' }
        ],
        6: [
          { id: 'w1d6t1', task: 'Code Review and Assessment', points: 100, time: 1.0, category: 'review', difficulty: 'easy' },
          { id: 'w1d6t2', task: 'Deploy to Railway.app', points: 150, time: 1.0, category: 'deployment', difficulty: 'medium' },
          { id: 'w1d6t3', task: 'Portfolio Documentation', points: 100, time: 1.0, category: 'portfolio', difficulty: 'easy' }
        ]
      },
      certificationFocus: "Google Cloud AI Fundamentals",
      projectGoal: "Bulletproof AI Data Processing System"
    }
  };

  // Achievements System
  const achievements = [
    { id: 'first_task', name: 'First Steps', description: 'Complete your first task', icon: '🎯', unlocked: false },
    { id: 'daily_streak_3', name: 'Consistent Learner', description: '3-day learning streak', icon: '🔥', unlocked: false },
    { id: 'week1_complete', name: 'Foundation Master', description: 'Complete Week 1', icon: '🏆', unlocked: false },
    { id: 'error_handler', name: 'Error Handler', description: 'Master exception handling', icon: '🛡️', unlocked: false },
    { id: 'pipeline_builder', name: 'Pipeline Builder', description: 'Build AI processing pipeline', icon: '⚙️', unlocked: false },
    { id: 'production_ready', name: 'Production Ready', description: 'Deploy production system', icon: '🚀', unlocked: false }
  ];

  // Spaced Repetition System
  const generateReviewItems = () => {
    const completed = Array.from(completedTasks);
    const reviewItems = completed.filter(taskId => {
      // Simple spaced repetition: review completed items after 1, 3, 7 days
      const completionDate = localStorage.getItem(`completion_${taskId}`);
      if (!completionDate) return false;
      
      const daysSince = Math.floor((Date.now() - parseInt(completionDate)) / (1000 * 60 * 60 * 24));
      return [1, 3, 7, 14].includes(daysSince);
    });
    
    return reviewItems;
  };

  // Task Completion Handler with Enhanced Features
  const completeTask = (taskId, points, category) => {
    if (completedTasks.has(taskId)) return;

    // Update completion state
    const newCompleted = new Set([...completedTasks, taskId]);
    setCompletedTasks(newCompleted);
    
    // Add XP with category multipliers
    const multiplier = category === 'capstone' ? 1.5 : category === 'project' ? 1.2 : 1.0;
    const earnedXP = Math.floor(points * multiplier);
    setTotalXP(prev => prev + earnedXP);
    setDailyXP(prev => prev + earnedXP);
    
    // Store completion date for spaced repetition
    localStorage.setItem(`completion_${taskId}`, Date.now().toString());
    
    // Check for portfolio items
    if (category === 'project' || category === 'capstone') {
      setPortfolioItems(prev => [...prev, {
        id: taskId,
        name: getCurrentTask(taskId)?.task || 'Project',
        completedDate: new Date().toISOString(),
        type: category
      }]);
    }
    
    // Update certification progress
    const progressIncrease = category === 'ai' ? 5 : category === 'production' ? 3 : 1;
    setCertificationProgress(prev => ({
      ...prev,
      'Google Cloud AI': Math.min(100, prev['Google Cloud AI'] + progressIncrease)
    }));
    
    // Show celebration
    setShowCelebration(true);
    setTimeout(() => setShowCelebration(false), 2000);
    
    // Note: saveProgressToBackend() will be called by useEffect when state updates
  };

  // Mark task as struggled (difficulty calibration)
  const markStruggled = (taskId) => {
    setStruggleTasks(prev => new Set([...prev, taskId]));
    // Adjust future difficulty based on struggle patterns
    const struggleCount = struggledTasks.size;
    if (struggleCount > 3) {
      setDifficultyLevel('easy');
    } else if (struggleCount < 2) {
      setDifficultyLevel('hard');
    }
  };

  // Notes Management
  const updateNotes = (taskId, noteContent) => {
    setNotes(prev => ({
      ...prev,
      [taskId]: noteContent
    }));
    saveProgressToBackend();
  };

  // Backend Integration (Railway.app)
  const saveProgressToBackend = async () => {
    
    try {
      const progressData = {
        currentWeek,
        currentDay,
        totalXP,
        dailyXP,
        streak,
        completedTasks: Array.from(completedTasks),
        struggledTasks: Array.from(struggledTasks),
        notes,
        portfolioItems,
        certificationProgress,
        difficultyLevel,
        lastUpdated: new Date().toISOString()
      };

      // Backend URL (replace this with the '/api/' with 'Railway.app URL/api/')
      

      const response = await fetch(`${API_BASE_URL}/api/progress`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(progressData)
      });

      if (!response.ok) {
        throw new Error('Failed to save progress');
      }
    } catch (error) {
      console.error('Error saving progress:', error);
      // Fallback to localStorage
      localStorage.setItem('aiProgressData', JSON.stringify({
        currentWeek, currentDay, totalXP, dailyXP, streak,
        completedTasks: Array.from(completedTasks),
        struggledTasks: Array.from(struggledTasks),
        notes, portfolioItems, certificationProgress, difficultyLevel
      }));
    }
  };

  // Load progress from backend/localStorage
  const loadProgress = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/progress`);
      if (response.ok) {
        const data = await response.json();
        setCurrentWeek(data.currentWeek || 1);
        setCurrentDay(data.currentDay || 1);
        setTotalXP(data.totalXP || 0);
        setDailyXP(data.dailyXP || 0);
        setStreak(data.streak || 0);
        setCompletedTasks(new Set(data.completedTasks || []));
        setStruggleTasks(new Set(data.struggledTasks || []));
        setNotes(data.notes || {});
        setPortfolioItems(data.portfolioItems || []);
        setCertificationProgress(data.certificationProgress || {
          'Google Cloud AI': 0, 'AWS ML Specialty': 0, 'Azure AI Engineer': 0
        });
        setDifficultyLevel(data.difficultyLevel || 'medium');
      }
    } catch (error) {
      // Fallback to localStorage
      const saved = localStorage.getItem('aiProgressData');
      if (saved) {
        const data = JSON.parse(saved);
        setCurrentWeek(data.currentWeek || 1);
        setCurrentDay(data.currentDay || 1);
        setTotalXP(data.totalXP || 0);
        setDailyXP(data.dailyXP || 0);
        setStreak(data.streak || 0);
        setCompletedTasks(new Set(data.completedTasks || []));
        setStruggleTasks(new Set(data.struggledTasks || []));
        setNotes(data.notes || {});
        setPortfolioItems(data.portfolioItems || []);
        setCertificationProgress(data.certificationProgress || {
          'Google Cloud AI': 0, 'AWS ML Specialty': 0, 'Azure AI Engineer': 0
        });
        setDifficultyLevel(data.difficultyLevel || 'medium');
      }
    }
  };

  // Helper functions
  const getCurrentTask = (taskId) => {
    const week = curriculum[currentWeek];
    if (!week) return null;
    
    for (const day of Object.keys(week.dailyTasks)) {
      const task = week.dailyTasks[day].find(t => t.id === taskId);
      if (task) return task;
    }
    return null;
  };

  const getTodaysTasks = () => {
    const week = curriculum[currentWeek];
    return week?.dailyTasks[currentDay] || [];
  };

  const getWeekProgress = () => {
    const week = curriculum[currentWeek];
    if (!week) return 0;
    
    let totalTasks = 0;
    let completedCount = 0;
    
    Object.values(week.dailyTasks).forEach(dayTasks => {
      totalTasks += dayTasks.length;
      dayTasks.forEach(task => {
        if (completedTasks.has(task.id)) completedCount++;
      });
    });
    
    return totalTasks > 0 ? (completedCount / totalTasks) * 100 : 0;
  };

  const getDifficultyColor = (difficulty) => {
    switch (difficulty) {
      case 'easy': return 'text-green-600 bg-green-100';
      case 'medium': return 'text-yellow-600 bg-yellow-100';
      case 'hard': return 'text-orange-600 bg-orange-100';
      case 'expert': return 'text-red-600 bg-red-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getCategoryIcon = (category) => {
    switch (category) {
      case 'foundation': return <Book className="w-4 h-4" />;
      case 'ai': return <Brain className="w-4 h-4" />;
      case 'coding': return <Code className="w-4 h-4" />;
      case 'project': return <Target className="w-4 h-4" />;
      case 'production': return <Settings className="w-4 h-4" />;
      case 'monitoring': return <BarChart3 className="w-4 h-4" />;
      case 'capstone': return <Trophy className="w-4 h-4" />;
      case 'deployment': return <Database className="w-4 h-4" />;
      case 'portfolio': return <Star className="w-4 h-4" />;
      default: return <Circle className="w-4 h-4" />;
    }
  };

  // Load progress on component mount
  useEffect(() => {
    loadProgress();
  }, []);

  // Update spaced repetition queue
  useEffect(() => {
    setSpaceRepetitionQueue(generateReviewItems());
  }, [completedTasks]);

  // Save progress whenever key state changes
  useEffect(() => {
    // Only save if we have some meaningful data (not initial load)
    if (completedTasks.size > 0 || totalXP > 0) {
      saveProgressToBackend();
    }
  }, [completedTasks, totalXP, portfolioItems, certificationProgress, notes]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      {/* Header */}
      <div className="max-w-6xl mx-auto mb-6">
        <div className="bg-white rounded-xl shadow-lg p-6">
          <div className="flex justify-between items-center mb-4">
            <div>
              <h1 className="text-3xl font-bold text-gray-800">AI Engineer Progress Tracker</h1>
              <p className="text-gray-600">Week {currentWeek}, Day {currentDay} • {curriculum[currentWeek]?.theme}</p>
            </div>
            <div className="flex items-center space-x-4">
              <div className="text-right">
                <div className="flex items-center text-xl font-bold text-blue-600">
                  <Zap className="w-5 h-5 mr-1" />
                  {totalXP.toLocaleString()} XP
                </div>
                <div className="text-sm text-gray-500">+{dailyXP} today</div>
              </div>
              <div className="text-right">
                <div className="flex items-center text-lg font-semibold text-orange-600">
                  <Flame className="w-5 h-5 mr-1" />
                  {streak} day streak
                </div>
                <div className="text-sm text-gray-500">Keep it up!</div>
              </div>
            </div>
          </div>
          
          {/* Week Progress Bar */}
          <div className="bg-gray-200 rounded-full h-3 mb-2">
            <div 
              className="bg-gradient-to-r from-blue-500 to-purple-600 h-3 rounded-full transition-all duration-500"
              style={{ width: `${getWeekProgress()}%` }}
            ></div>
          </div>
          <div className="text-sm text-gray-600">Week {currentWeek} Progress: {getWeekProgress().toFixed(1)}%</div>
        </div>
      </div>

      <div className="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Content - Today's Tasks */}
        <div className="lg:col-span-2 space-y-6">
          {/* Today's Focus */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h2 className="text-2xl font-bold mb-4 flex items-center">
              <Target className="w-6 h-6 mr-2 text-blue-600" />
              Today's Focus
            </h2>
            <div className="space-y-4">
              {getTodaysTasks().map((task, index) => (
                <div key={task.id} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
                  <div className="flex items-start justify-between">
                    <div className="flex items-start space-x-3 flex-1">
                      <button
                        onClick={() => completeTask(task.id, task.points, task.category)}
                        className="mt-1"
                      >
                        {completedTasks.has(task.id) ? (
                          <CheckCircle2 className="w-6 h-6 text-green-600" />
                        ) : (
                          <Circle className="w-6 h-6 text-gray-400 hover:text-blue-600" />
                        )}
                      </button>
                      
                      <div className="flex-1">
                        <div className="flex items-center space-x-2 mb-2">
                          {getCategoryIcon(task.category)}
                          <h3 className={`font-semibold ${completedTasks.has(task.id) ? 'line-through text-gray-500' : 'text-gray-800'}`}>
                            {task.task}
                          </h3>
                          <span className={`px-2 py-1 rounded text-xs font-medium ${getDifficultyColor(task.difficulty)}`}>
                            {task.difficulty}
                          </span>
                        </div>
                        
                        <div className="flex items-center space-x-4 text-sm text-gray-600 mb-3">
                          <span className="flex items-center">
                            <Zap className="w-4 h-4 mr-1" />
                            {task.points} XP
                          </span>
                          <span className="flex items-center">
                            <Clock className="w-4 h-4 mr-1" />
                            {task.time}h
                          </span>
                        </div>

                        {/* Notes Section */}
                        <div className="space-y-2">
                          <textarea
                            placeholder="Add your notes, insights, or struggles here..."
                            value={notes[task.id] || ''}
                            onChange={(e) => updateNotes(task.id, e.target.value)}
                            className="w-full p-2 border rounded-md text-sm resize-none"
                            rows="2"
                          />
                          
                          {!completedTasks.has(task.id) && (
                            <div className="flex space-x-2">
                              <button
                                onClick={() => markStruggled(task.id)}
                                className={`px-3 py-1 rounded text-xs ${
                                  struggledTasks.has(task.id) 
                                    ? 'bg-red-100 text-red-700' 
                                    : 'bg-gray-100 text-gray-600 hover:bg-red-50'
                                }`}
                              >
                                😅 This is challenging
                              </button>
                            </div>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Spaced Repetition Review */}
          {spaceRepetitionQueue.length > 0 && (
            <div className="bg-yellow-50 border border-yellow-200 rounded-xl p-6">
              <h3 className="text-lg font-semibold mb-3 flex items-center text-yellow-800">
                <Brain className="w-5 h-5 mr-2" />
                Quick Review ({spaceRepetitionQueue.length} items)
              </h3>
              <p className="text-sm text-yellow-700 mb-3">
                Review these previously completed concepts to strengthen your memory:
              </p>
              <div className="space-y-2">
                {spaceRepetitionQueue.slice(0, 3).map(taskId => {
                  const task = getCurrentTask(taskId);
                  return task ? (
                    <div key={taskId} className="flex items-center space-x-2 text-sm">
                      <MessageSquare className="w-4 h-4" />
                      <span>{task.task}</span>
                    </div>
                  ) : null;
                })}
              </div>
            </div>
          )}
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Quick Stats */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h3 className="text-lg font-semibold mb-4">Quick Stats</h3>
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-gray-600">Tasks Completed</span>
                <span className="font-semibold">{completedTasks.size}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Current Difficulty</span>
                <span className={`px-2 py-1 rounded text-xs font-medium ${getDifficultyColor(difficultyLevel)}`}>
                  {difficultyLevel}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Portfolio Items</span>
                <span className="font-semibold">{portfolioItems.length}</span>
              </div>
            </div>
          </div>

          {/* Certification Progress */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h3 className="text-lg font-semibold mb-4 flex items-center">
              <Trophy className="w-5 h-5 mr-2 text-yellow-600" />
              Certification Progress
            </h3>
            <div className="space-y-4">
              {Object.entries(certificationProgress).map(([cert, progress]) => (
                <div key={cert}>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-gray-600">{cert}</span>
                    <span className="font-medium">{progress}%</span>
                  </div>
                  <div className="bg-gray-200 rounded-full h-2">
                    <div 
                      className="bg-gradient-to-r from-yellow-400 to-yellow-600 h-2 rounded-full transition-all duration-500"
                      style={{ width: `${progress}%` }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Achievements */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h3 className="text-lg font-semibold mb-4 flex items-center">
              <Star className="w-5 h-5 mr-2 text-purple-600" />
              Achievements
            </h3>
            <div className="space-y-2">
              {achievements.slice(0, 4).map((achievement) => {
                const unlocked = (
                  achievement.id === 'first_task' && completedTasks.size > 0
                ) || (
                  achievement.id === 'error_handler' && completedTasks.size >= 3
                ) || (
                  achievement.id === 'pipeline_builder' && portfolioItems.length > 0
                );
                
                return (
                  <div key={achievement.id} className={`flex items-center space-x-2 p-2 rounded ${unlocked ? 'bg-green-50' : 'bg-gray-50'}`}>
                    <span className="text-lg">{achievement.icon}</span>
                    <div>
                      <div className={`text-sm font-medium ${unlocked ? 'text-green-800' : 'text-gray-500'}`}>
                        {achievement.name}
                      </div>
                      <div className="text-xs text-gray-500">{achievement.description}</div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Navigation */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h3 className="text-lg font-semibold mb-4">Navigation</h3>
            <div className="space-y-2">
              <button
                onClick={() => setCurrentDay(Math.max(1, currentDay - 1))}
                disabled={currentDay === 1}
                className="w-full p-2 text-left text-sm bg-gray-100 rounded hover:bg-gray-200 disabled:opacity-50"
              >
                ← Previous Day
              </button>
              <button
                onClick={() => setCurrentDay(Math.min(6, currentDay + 1))}
                disabled={currentDay === 6}
                className="w-full p-2 text-left text-sm bg-blue-100 text-blue-700 rounded hover:bg-blue-200 disabled:opacity-50"
              >
                Next Day →
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Celebration Modal */}
      {showCelebration && (
        <div className="fixed inset-0 flex items-center justify-center z-50 bg-black bg-opacity-50">
          <div className="bg-white rounded-xl p-8 text-center max-w-sm mx-4 transform animate-bounce">
            <div className="text-6xl mb-4">🎉</div>
            <h3 className="text-2xl font-bold text-gray-800 mb-2">Awesome!</h3>
            <p className="text-gray-600 mb-4">You earned {dailyXP} XP! Keep building your AI engineering skills!</p>
            <div className="text-3xl">⚡ +{dailyXP} XP</div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AIProgressTracker;
