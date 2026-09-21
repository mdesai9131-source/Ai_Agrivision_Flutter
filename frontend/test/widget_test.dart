import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:ai_agrivision/models/disease_model.dart';
import 'package:ai_agrivision/models/prediction_model.dart';
import 'package:ai_agrivision/models/user_model.dart';
import 'package:ai_agrivision/models/agro_location_model.dart';
import 'package:ai_agrivision/models/address_suggestion_model.dart';
import 'package:ai_agrivision/widgets/confidence_indicator.dart';
import 'package:ai_agrivision/widgets/severity_badge.dart';

void main() {
  group('Dart Data Models Tests', () {
    test('UserModel serialization and deserialization', () {
      final json = {
        'id': 'user_001',
        'name': 'Kisan Lal',
        'email': 'kisan@example.com',
        'phone': '9876543210',
        'location': {
          'latitude': 23.25,
          'longitude': 77.41,
          'city': 'Bhopal',
          'state': 'MP'
        }
      };

      final user = UserModel.fromJson(json);
      expect(user.id, 'user_001');
      expect(user.name, 'Kisan Lal');
      expect(user.location.city, 'Bhopal');
      expect(user.location.latitude, 23.25);
    });

    test('PredictionModel confidence threshold categorization', () {
      final highConf = PredictionModel(
        id: 'p1',
        userId: 'u1',
        imageUrl: 'http://example.com/leaf.jpg',
        crop: 'Tomato',
        disease: 'Early Blight',
        confidence: 0.94,
        status: 'high_confidence',
      );
      expect(highConf.isHighConfidence, true);
      expect(highConf.isUncertain, false);

      final uncertain = PredictionModel(
        id: 'p2',
        userId: 'u1',
        imageUrl: 'http://example.com/blur.jpg',
        crop: null,
        disease: null,
        confidence: 0.45,
        status: 'uncertain',
      );
      expect(uncertain.isUncertain, true);
      expect(uncertain.isHighConfidence, false);
    });

    test('DiseaseModel safe recommendations structure', () {
      final rec = DiseaseModel(
        disease: 'Tomato Early Blight',
        description: 'Fungal leaf spotting',
        symptoms: ['Concentric rings on foliage'],
        prevention: ['Avoid overhead irrigation'],
        management: ['Sanitize tools between plots'],
        expertRequired: false,
      );

      expect(rec.symptoms.length, 1);
      expect(rec.prevention.length, 1);
      expect(rec.expertRequired, false);
    });
  });

  group('Widget Tests', () {
    testWidgets('ConfidenceIndicator displays percentage and high confidence status', (WidgetTester tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: ConfidenceIndicator(
              confidence: 0.92,
              status: 'high_confidence',
            ),
          ),
        ),
      );

      expect(find.text('92%'), findsOneWidget);
      expect(find.text('High Confidence'), findsOneWidget);
    });

    testWidgets('SeverityBadge renders Not Available disclosure correctly', (WidgetTester tester) async {
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: SeverityBadge(
              severity: null,
              severityAvailable: false,
              severityMessage: 'Severity requires lesion segmentation.',
            ),
          ),
        ),
      );

      expect(find.text('Severity: Not Available'), findsOneWidget);
    });

    test('Wheat PredictionModel accurately preserves crop and disease metadata', () {
      final wheatPred = PredictionModel(
        id: 'p_wheat_1',
        userId: 'u_test',
        imageUrl: 'http://example.com/wheat_rust.jpg',
        crop: 'Wheat',
        disease: 'Wheat Brown Rust',
        confidence: 0.91,
        status: 'high_confidence',
      );

      expect(wheatPred.crop, 'Wheat');
      expect(wheatPred.disease, 'Wheat Brown Rust');
      expect(wheatPred.isHighConfidence, true);
      expect(wheatPred.isHealthy, false);
    });

    test('AgroLocationModel parses agricultural center coordinates correctly', () {
      final json = {
        'id': 'center_kvk_01',
        'name': 'District Krishi Vigyan Kendra',
        'category': 'Agro Office & Research',
        'address': 'Main Mandi Road',
        'latitude': 23.284,
        'longitude': 77.432,
        'distanceKm': 3.2,
        'rating': 4.8,
        'phone': '+91 1800-180-1551',
        'services': ['Soil Testing', 'Pathologist Advice']
      };

      final center = AgroLocationModel.fromJson(json);
      expect(center.id, 'center_kvk_01');
      expect(center.name, 'District Krishi Vigyan Kendra');
      expect(center.latitude, 23.284);
      expect(center.longitude, 77.432);
      expect(center.distanceKm, 3.2);
      expect(center.services.length, 2);
    });

    test('AddressSuggestion parses OpenStreetMap Nominatim response correctly', () {
      final nominatimJson = {
        'display_name': 'Sarkhej, Vejalpur Taluka, Ahmedabad, Gujarat, 380051, India',
        'lat': '23.0040',
        'lon': '72.5087',
        'address': {
          'town': 'Sarkhej',
          'state_district': 'Ahmedabad',
          'state': 'Gujarat',
          'country': 'India',
        }
      };

      final suggestion = AddressSuggestion.fromNominatimJson(nominatimJson);
      expect(suggestion.title, 'Sarkhej, Ahmedabad');
      expect(suggestion.subtitle.contains('Gujarat'), true);
      expect(suggestion.latitude, 23.0040);
      expect(suggestion.longitude, 72.5087);
      expect(suggestion.district, 'Ahmedabad');
    });

    test('AddressSuggestion correctly parses Surendranagar district response', () {
      final surendranagarJson = {
        'display_name': 'Bala Road, Wadhwan, Surendranagar, Gujarat, 363030, India',
        'lat': '22.7284',
        'lon': '71.6371',
        'address': {
          'road': 'Bala Road',
          'town': 'Wadhwan',
          'state_district': 'Surendranagar',
          'state': 'Gujarat',
          'country': 'India',
        }
      };

      final suggestion = AddressSuggestion.fromNominatimJson(surendranagarJson);
      expect(suggestion.title, 'Wadhwan, Surendranagar');
      expect(suggestion.district, 'Surendranagar');
      expect(suggestion.latitude, 22.7284);
      expect(suggestion.longitude, 71.6371);
    });
  });
}
