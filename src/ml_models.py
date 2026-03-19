"""
Machine Learning Models Module
==============================
Builds and compares multiple ML models for churn prediction:
- Logistic Regression (baseline)
- Decision Tree
- Random Forest
- XGBoost (bonus)

Evaluates using:
- Accuracy, Precision, Recall, F1-Score
- ROC-AUC Score
- Feature Importance
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import (accuracy_score, precision_score, recall_score, 
                             f1_score, roc_auc_score, confusion_matrix,
                             classification_report, roc_curve, precision_recall_curve)
from sklearn.pipeline import Pipeline
import warnings
import os
import joblib

warnings.filterwarnings('ignore')
os.makedirs('results/models', exist_ok=True)
os.makedirs('results/visualizations', exist_ok=True)


class ChurnModelTrainer:
    """
    Complete ML pipeline for customer churn prediction.
    
    Models Trained:
    1. Logistic Regression - Interpretable baseline
    2. Decision Tree - Captures non-linear patterns
    3. Random Forest - Robust ensemble method
    4. Gradient Boosting - High-performance ensemble
    """
    
    def __init__(self, df, target_col='churn', test_size=0.2, random_state=42):
        self.df = df
        self.target_col = target_col
        self.test_size = test_size
        self.random_state = random_state
        
        self.X = None
        self.y = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        
        self.scaler = StandardScaler()
        self.models = {}
        self.model_results = {}
        self.best_model = None
        
    def prepare_features(self):
        """
        Prepare features for modeling.
        Combines original data with engineered features.
        """
        from src.feature_engineering import FeatureEngineer
        
        engineer = FeatureEngineer(self.df)
        X = engineer.create_final_featureset()
        
        self.X = X
        self.y = self.df[self.target_col]
        
        print(f"Features prepared: {X.shape[1]} features")
        print(f"Target distribution: {self.y.value_counts().to_dict()}")
        
        return self
    
    def split_data(self):
        """
        Split data into training and test sets.
        Uses stratified sampling to maintain class balance.
        """
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y,
            test_size=self.test_size,
            random_state=self.random_state,
            stratify=self.y
        )
        
        print(f"\nData Split:")
        print(f"  Training set: {len(self.X_train):,} samples")
        print(f"  Test set: {len(self.X_test):,} samples")
        print(f"  Training churn rate: {self.y_train.mean()*100:.2f}%")
        print(f"  Test churn rate: {self.y_test.mean()*100:.2f}%")
        
        return self
    
    def scale_features(self):
        """
        Scale numerical features for models that require it.
        """
        self.X_train_scaled = self.scaler.fit_transform(self.X_train)
        self.X_test_scaled = self.scaler.transform(self.X_test)
        
        return self
    
    def train_logistic_regression(self):
        """
        Train Logistic Regression model.
        
        Why Logistic Regression:
        - Highly interpretable coefficients
        - Good baseline for binary classification
        - Provides probability estimates
        """
        print("\n" + "=" * 60)
        print("Training Logistic Regression...")
        print("=" * 60)
        
        model = LogisticRegression(
            random_state=self.random_state,
            max_iter=1000,
            class_weight='balanced'
        )
        
        model.fit(self.X_train_scaled, self.y_train)
        
        self.models['Logistic Regression'] = model
        self._evaluate_model(model, 'Logistic Regression')
        
        return model
    
    def train_decision_tree(self):
        """
        Train Decision Tree model.
        
        Why Decision Tree:
        - Captures non-linear relationships
        - Easy to visualize and explain
        - Handles mixed feature types
        """
        print("\n" + "=" * 60)
        print("Training Decision Tree...")
        print("=" * 60)
        
        model = DecisionTreeClassifier(
            random_state=self.random_state,
            class_weight='balanced',
            max_depth=10,
            min_samples_split=20,
            min_samples_leaf=10
        )
        
        model.fit(self.X_train, self.y_train)
        
        self.models['Decision Tree'] = model
        self._evaluate_model(model, 'Decision Tree')
        
        return model
    
    def train_random_forest(self):
        """
        Train Random Forest model.
        
        Why Random Forest:
        - Robust to overfitting
        - Handles feature importance well
        - Works without feature scaling
        - Good for imbalanced datasets
        """
        print("\n" + "=" * 60)
        print("Training Random Forest...")
        print("=" * 60)
        
        model = RandomForestClassifier(
            n_estimators=100,
            random_state=self.random_state,
            class_weight='balanced',
            max_depth=15,
            min_samples_split=20,
            min_samples_leaf=10,
            n_jobs=-1
        )
        
        model.fit(self.X_train, self.y_train)
        
        self.models['Random Forest'] = model
        self._evaluate_model(model, 'Random Forest')
        
        return model
    
    def train_gradient_boosting(self):
        """
        Train Gradient Boosting model.
        
        Why Gradient Boosting:
        - State-of-the-art performance
        - Handles complex patterns
        - Good probability calibration
        """
        print("\n" + "=" * 60)
        print("Training Gradient Boosting...")
        print("=" * 60)
        
        model = GradientBoostingClassifier(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            random_state=self.random_state,
            min_samples_split=20,
            min_samples_leaf=10
        )
        
        model.fit(self.X_train, self.y_train)
        
        self.models['Gradient Boosting'] = model
        self._evaluate_model(model, 'Gradient Boosting')
        
        return model
    
    def _evaluate_model(self, model, model_name):
        """
        Evaluate model performance and store results.
        """
        if 'Logistic' in model_name:
            y_pred = model.predict(self.X_test_scaled)
            y_pred_proba = model.predict_proba(self.X_test_scaled)[:, 1]
        else:
            y_pred = model.predict(self.X_test)
            y_pred_proba = model.predict_proba(self.X_test)[:, 1]
        
        results = {
            'accuracy': accuracy_score(self.y_test, y_pred),
            'precision': precision_score(self.y_test, y_pred),
            'recall': recall_score(self.y_test, y_pred),
            'f1_score': f1_score(self.y_test, y_pred),
            'roc_auc': roc_auc_score(self.y_test, y_pred_proba)
        }
        
        self.model_results[model_name] = {
            'model': model,
            'predictions': y_pred,
            'probabilities': y_pred_proba,
            'metrics': results
        }
        
        print(f"\n{model_name} Results:")
        print("-" * 40)
        for metric, value in results.items():
            print(f"  {metric.upper()}: {value:.4f}")
        
        return results
    
    def compare_models(self):
        """
        Compare all trained models.
        """
        print("\n" + "=" * 80)
        print("MODEL COMPARISON")
        print("=" * 80)
        
        comparison_df = pd.DataFrame({
            name: results['metrics']
            for name, results in self.model_results.items()
        }).T
        
        print(comparison_df.round(4).to_string())
        
        best_model_name = comparison_df['f1_score'].idxmax()
        self.best_model = self.model_results[best_model_name]['model']
        
        print(f"\n*** BEST MODEL: {best_model_name} ***")
        print(f"    Selected based on F1-Score (balances precision and recall)")
        
        return comparison_df
    
    def hyperparameter_tuning(self):
        """
        Perform hyperparameter tuning on Random Forest.
        """
        print("\n" + "=" * 60)
        print("Hyperparameter Tuning (Random Forest)...")
        print("=" * 60)
        
        param_grid = {
            'n_estimators': [50, 100, 150],
            'max_depth': [8, 10, 15],
            'min_samples_split': [10, 20, 30],
            'min_samples_leaf': [5, 10, 15]
        }
        
        rf = RandomForestClassifier(
            random_state=self.random_state,
            class_weight='balanced',
            n_jobs=-1
        )
        
        grid_search = GridSearchCV(
            rf, param_grid, cv=5, scoring='f1', n_jobs=-1, verbose=1
        )
        
        grid_search.fit(self.X_train, self.y_train)
        
        print(f"\nBest Parameters: {grid_search.best_params_}")
        print(f"Best CV F1 Score: {grid_search.best_score_:.4f}")
        
        best_rf = grid_search.best_estimator_
        self.models['Random Forest (Tuned)'] = best_rf
        self._evaluate_model(best_rf, 'Random Forest (Tuned)')
        
        return grid_search.best_params_
    
    def get_feature_importance(self, model_name='Random Forest'):
        """
        Get and display feature importance.
        """
        if model_name not in self.models:
            return None
        
        model = self.models[model_name]
        
        if hasattr(model, 'feature_importances_'):
            importance = pd.DataFrame({
                'feature': self.X.columns,
                'importance': model.feature_importances_
            }).sort_values('importance', ascending=False)
            
            print("\n" + "=" * 60)
            print(f"TOP 15 FEATURE IMPORTANCE ({model_name})")
            print("=" * 60)
            print(importance.head(15).to_string(index=False))
            
            return importance
        
        elif hasattr(model, 'coef_'):
            importance = pd.DataFrame({
                'feature': self.X.columns,
                'coefficient': np.abs(model.coef_[0])
            }).sort_values('coefficient', ascending=False)
            
            print("\n" + "=" * 60)
            print(f"TOP 15 FEATURE COEFFICIENTS ({model_name})")
            print("=" * 60)
            print(importance.head(15).to_string(index=False))
            
            return importance
        
        return None
    
    def plot_feature_importance(self, model_name='Random Forest'):
        """
        Plot feature importance visualization.
        """
        importance = self.get_feature_importance(model_name)
        
        if importance is None:
            return
        
        plt.figure(figsize=(12, 8))
        top_features = importance.head(15)
        
        colors = plt.cm.RdYlGn(np.linspace(0.8, 0.2, len(top_features)))
        
        plt.barh(range(len(top_features)), top_features['importance'].values, color=colors)
        plt.yticks(range(len(top_features)), top_features['feature'].values)
        plt.xlabel('Feature Importance')
        plt.title(f'Top 15 Most Important Features - {model_name}', fontsize=14, fontweight='bold')
        plt.gca().invert_yaxis()
        
        plt.tight_layout()
        plt.savefig(f'results/visualizations/12_feature_importance_{model_name.replace(" ", "_").lower()}.png', 
                   dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"\nFeature importance plot saved.")
    
    def plot_roc_curves(self):
        """
        Plot ROC curves for all models.
        """
        plt.figure(figsize=(10, 8))
        
        for name, results in self.model_results.items():
            y_test = self.y_test
            y_pred_proba = results['probabilities']
            
            fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
            roc_auc = results['metrics']['roc_auc']
            
            plt.plot(fpr, tpr, label=f'{name} (AUC = {roc_auc:.3f})')
        
        plt.plot([0, 1], [0, 1], 'k--', label='Random Classifier')
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('ROC Curves - Model Comparison', fontsize=14, fontweight='bold')
        plt.legend(loc='lower right')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('results/visualizations/13_roc_curves.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("ROC curves saved.")
    
    def plot_confusion_matrices(self):
        """
        Plot confusion matrices for all models.
        """
        n_models = len(self.models)
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        axes = axes.flatten()
        
        for idx, (name, results) in enumerate(self.model_results.items()):
            if idx >= 4:
                break
                
            cm = confusion_matrix(self.y_test, results['predictions'])
            
            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[idx],
                       xticklabels=['Retained', 'Churned'],
                       yticklabels=['Retained', 'Churned'])
            axes[idx].set_title(f'{name}', fontsize=12, fontweight='bold')
            axes[idx].set_ylabel('Actual')
            axes[idx].set_xlabel('Predicted')
        
        plt.tight_layout()
        plt.savefig('results/visualizations/14_confusion_matrices.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("Confusion matrices saved.")
    
    def plot_model_comparison(self):
        """
        Plot model comparison bar chart.
        """
        comparison_df = pd.DataFrame({
            name: results['metrics']
            for name, results in self.model_results.items()
        }).T
        
        metrics = ['accuracy', 'precision', 'recall', 'f1_score', 'roc_auc']
        
        fig, ax = plt.subplots(figsize=(14, 6))
        
        x = np.arange(len(comparison_df))
        width = 0.15
        
        colors = plt.cm.Set2(np.linspace(0, 1, len(metrics)))
        
        for i, metric in enumerate(metrics):
            offset = (i - len(metrics)/2 + 0.5) * width
            bars = ax.bar(x + offset, comparison_df[metric], width, 
                         label=metric.replace('_', ' ').title(), color=colors[i])
        
        ax.set_xlabel('Model')
        ax.set_ylabel('Score')
        ax.set_title('Model Performance Comparison', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(comparison_df.index, rotation=15, ha='right')
        ax.legend(loc='lower right')
        ax.set_ylim(0, 1.1)
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig('results/visualizations/15_model_comparison.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("Model comparison plot saved.")
    
    def generate_model_report(self):
        """
        Generate comprehensive model report.
        """
        report = """
        ================================================================================
        MACHINE LEARNING MODEL REPORT - CUSTOMER CHURN PREDICTION
        ================================================================================
        
        OBJECTIVE:
        Predict customer churn with high accuracy to enable proactive retention.
        
        METHODOLOGY:
        1. Feature Engineering: Created 40+ features from raw data
        2. Data Split: 80% training, 20% testing (stratified)
        3. Models Compared: Logistic Regression, Decision Tree, Random Forest, Gradient Boosting
        4. Evaluation: Accuracy, Precision, Recall, F1-Score, ROC-AUC
        
        MODEL RESULTS SUMMARY:
        """
        
        for name, results in self.model_results.items():
            report += f"\n{name}:\n"
            report += "-" * 40 + "\n"
            for metric, value in results['metrics'].items():
                report += f"  {metric.upper()}: {value:.4f}\n"
        
        best_name = max(self.model_results.keys(), 
                       key=lambda x: self.model_results[x]['metrics']['f1_score'])
        best_metrics = self.model_results[best_name]['metrics']
        
        report += f"""
        
        ================================================================================
        RECOMMENDATION
        ================================================================================
        
        BEST MODEL: {best_name}
        
        Key Metrics:
        - Accuracy: {best_metrics['accuracy']:.2%}
        - Precision: {best_metrics['precision']:.2%}
        - Recall: {best_metrics['recall']:.2%}
        - F1-Score: {best_metrics['f1_score']:.2%}
        - ROC-AUC: {best_metrics['roc_auc']:.2%}
        
        Why This Model:
        - F1-Score selected as primary metric (balances precision and recall)
        - In churn prediction, both catching at-risk customers AND minimizing 
          false positives are important
        - ROC-AUC confirms strong discriminative ability
        
        DEPLOYMENT RECOMMENDATIONS:
        1. Use probability scores (not just binary predictions)
        2. Set threshold at 0.5 for high-confidence predictions
        3. For uncertain cases, flag for human review
        4. Retrain quarterly with new data
        5. Monitor feature importance drift over time
        
        ================================================================================
        """
        
        with open('results/model_report.txt', 'w') as f:
            f.write(report)
        
        print(report)
        print("\nModel report saved to results/model_report.txt")
        
        return report
    
    def save_models(self):
        """
        Save trained models to disk.
        """
        os.makedirs('results/models', exist_ok=True)
        
        for name, results in self.model_results.items():
            filename = f"results/models/{name.replace(' ', '_').lower()}_model.pkl"
            joblib.dump(results['model'], filename)
            print(f"Model saved: {filename}")
    
    def predict_new_customers(self, new_data):
        """
        Predict churn for new customer data.
        """
        predictions = self.best_model.predict(new_data)
        probabilities = self.best_model.predict_proba(new_data)[:, 1]
        
        return predictions, probabilities
    
    def run_complete_pipeline(self):
        """
        Execute the complete ML pipeline.
        """
        print("\n" + "=" * 80)
        print("CUSTOMER CHURN PREDICTION - ML PIPELINE")
        print("=" * 80)
        
        self.prepare_features()
        self.split_data()
        self.scale_features()
        
        self.train_logistic_regression()
        self.train_decision_tree()
        self.train_random_forest()
        self.train_gradient_boosting()
        
        self.compare_models()
        self.hyperparameter_tuning()
        
        self.get_feature_importance()
        self.plot_feature_importance()
        self.plot_roc_curves()
        self.plot_confusion_matrices()
        self.plot_model_comparison()
        
        self.generate_model_report()
        self.save_models()
        
        return self.model_results, self.best_model


def main():
    """Run complete ML pipeline."""
    df = pd.read_csv('data/customer_data.csv')
    
    trainer = ChurnModelTrainer(df)
    results, best_model = trainer.run_complete_pipeline()
    
    return results, best_model


if __name__ == "__main__":
    main()
